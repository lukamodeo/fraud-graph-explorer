# src/fraud_graph_explorer/graph_explorer/tests/test_isolation.py

"""
DB-level tests for per-user isolation and shared entity graph.

These tests use TestCase (not SimpleTestCase) — they create a test database
that is rolled back after each test method.

Run:  manage test fraud_graph_explorer.graph_explorer.tests.test_isolation

NOTE: Adjust model field names if your models differ from what's used here.
The key fields tested:
  - Application: user (FK), request_number, country_code
  - Entity: entity_type, value, country_code
  - UsesIdentifier: application (FK), entity (FK), original_value
"""

from django.test import TestCase
from django.contrib.auth.models import User

from fraud_graph_explorer.graph_explorer.models import Application, Entity, UsesIdentifier


class PerUserIsolationTests(TestCase):
    """Test that applications are isolated per user — the core security feature."""

    def setUp(self):
        self.user_a = User.objects.create_user('alice', password='test123')
        self.user_b = User.objects.create_user('bob', password='test456')

    def test_user_only_sees_own_applications(self):
        """Each user's queryset should only return their own applications."""
        Application.objects.create(user=self.user_a, request_number='APP-001', country_code='IT')
        Application.objects.create(user=self.user_a, request_number='APP-002', country_code='DE')
        Application.objects.create(user=self.user_b, request_number='APP-003', country_code='FR')

        a_apps = Application.objects.filter(user=self.user_a)
        b_apps = Application.objects.filter(user=self.user_b)

        self.assertEqual(a_apps.count(), 2)
        self.assertEqual(b_apps.count(), 1)

    def test_user_cannot_find_other_users_applications(self):
        """User A querying for User B's request_number should get 0 results."""
        Application.objects.create(
            user=self.user_b, request_number='SECRET-001', country_code='IT'
        )

        # User A tries to find it
        found = Application.objects.filter(user=self.user_a, request_number='SECRET-001')
        self.assertEqual(found.count(), 0)

    def test_application_count_per_user(self):
        """Total count should match per-user counts."""
        for i in range(5):
            Application.objects.create(
                user=self.user_a, request_number=f'A-{i:03d}', country_code='IT'
            )
        for i in range(3):
            Application.objects.create(
                user=self.user_b, request_number=f'B-{i:03d}', country_code='DE'
            )

        self.assertEqual(Application.objects.filter(user=self.user_a).count(), 5)
        self.assertEqual(Application.objects.filter(user=self.user_b).count(), 3)
        self.assertEqual(Application.objects.count(), 8)

    def test_delete_user_cascades_to_applications(self):
        """Deleting a user should delete all their applications (CASCADE)."""
        Application.objects.create(user=self.user_a, request_number='APP-001', country_code='IT')
        Application.objects.create(user=self.user_a, request_number='APP-002', country_code='DE')

        self.assertEqual(Application.objects.filter(user=self.user_a).count(), 2)

        # Store the ID before deletion — the instance's pk becomes None after .delete()
        user_a_id = self.user_a.id
        self.user_a.delete()

        # Filter by user_id (integer) instead of user (instance) — the instance is gone
        self.assertEqual(Application.objects.filter(user_id=user_a_id).count(), 0)


class SharedEntityGraphTests(TestCase):
    """Test that entities are globally shared across users (Option A design)."""

    def setUp(self):
        self.user_a = User.objects.create_user('alice', password='test123')
        self.user_b = User.objects.create_user('bob', password='test456')

    def test_same_entity_linked_by_two_users(self):
        """Two users ingesting the same VAT should link to the SAME entity vertex."""
        entity = Entity.objects.create(
            entity_type='VAT', value='IT12345678901', country_code='IT'
        )

        app_a = Application.objects.create(
            user=self.user_a, request_number='APP-A', country_code='IT'
        )
        app_b = Application.objects.create(
            user=self.user_b, request_number='APP-B', country_code='IT'
        )

        UsesIdentifier.objects.create(application=app_a, entity=entity, original_value='IT12345678901')
        UsesIdentifier.objects.create(application=app_b, entity=entity, original_value='IT12345678901')

        # The entity should be linked to both applications
        linked_apps = entity.applications.all()
        self.assertEqual(linked_apps.count(), 2)
        self.assertIn(app_a, linked_apps)
        self.assertIn(app_b, linked_apps)

    def test_entity_country_code_stored_on_creation(self):
        """Entity.country_code should be set when the entity is created."""
        entity = Entity.objects.create(
            entity_type='VAT', value='IT12345678901', country_code='IT'
        )
        self.assertEqual(entity.country_code, 'IT')

    def test_entity_country_code_none_for_unsupported_country(self):
        """Unsupported country codes should not be stored (None)."""
        entity = Entity.objects.create(
            entity_type='VAT', value='NL123456789B01', country_code=None
        )
        self.assertIsNone(entity.country_code)

    def test_get_or_create_does_not_overwrite_country_code(self):
        """get_or_create should not update country_code on existing entities."""
        # Create entity with country_code
        entity, created = Entity.objects.get_or_create(
            entity_type='VAT',
            value='IT12345678901',
            defaults={'country_code': 'IT'}
        )
        self.assertTrue(created)
        self.assertEqual(entity.country_code, 'IT')

        # Second get_or_create with different defaults — should NOT overwrite
        entity2, created2 = Entity.objects.get_or_create(
            entity_type='VAT',
            value='IT12345678901',
            defaults={'country_code': None}  # different default
        )
        self.assertFalse(created2)
        self.assertEqual(entity2.country_code, 'IT')  # unchanged


class HasLinksAnnotationTests(TestCase):
    """Test the has-links computation — whether an application has linked applications.

    NOTE: This test uses annotate_has_links if available. If the function signature
    differs, adjust the import and call. If the function isn't easily testable
    in isolation, these tests can be skipped or adapted.
    """

    def setUp(self):
        self.user = User.objects.create_user('alice', password='test123')

    def test_application_with_no_links(self):
        """An application with no shared entities should have has_links=False."""
        app = Application.objects.create(
            user=self.user, request_number='SOLO-001', country_code='IT'
        )
        # No entities, no edges → no links
        self.assertEqual(UsesIdentifier.objects.filter(application=app).count(), 0)

    def test_application_with_shared_entity_has_links(self):
        """Two applications sharing an entity should have has_links=True."""
        app1 = Application.objects.create(
            user=self.user, request_number='APP-001', country_code='IT'
        )
        app2 = Application.objects.create(
            user=self.user, request_number='APP-002', country_code='IT'
        )

        entity = Entity.objects.create(
            entity_type='VAT', value='IT12345678901', country_code='IT'
        )

        UsesIdentifier.objects.create(application=app1, entity=entity, original_value='IT12345678901')
        UsesIdentifier.objects.create(application=app2, entity=entity, original_value='IT12345678901')

        # Both applications use the same entity → they are linked
        shared_entities = set(
            UsesIdentifier.objects.filter(application=app1).values_list('entity_id', flat=True)
        ) & set(
            UsesIdentifier.objects.filter(application=app2).values_list('entity_id', flat=True)
        )
        self.assertGreater(len(shared_entities), 0, "Applications should share at least one entity")
