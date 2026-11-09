# src/fraud_graph_explorer/graph_explorer/tests/test_typo.py

"""
Tests for inject_typo — the bulk_generate_pdfs typo injection helper.

Behavior:
  - Returns a string with a single random typo (substitute, delete, or insert)
  - Preserves the first 2 chars (country prefix for VAT/IBAN)
  - Returns the original value if it's too short (< 4 chars)
  - The typo should make the value different from the original

Run:  manage test graph_explorer.tests.test_typo
"""

import random

from django.test import SimpleTestCase

from fraud_graph_explorer.graph_explorer.management.commands.bulk_generate_pdfs import _inject_typo as inject_typo


class InjectTypoTests(SimpleTestCase):
    """Test the inject_typo function."""

    def setUp(self):
        """Seed the random generator for reproducible tests."""
        random.seed(42)

    # ─── Basic behavior ───
    def test_returns_string(self):
        result = inject_typo('IT12345678901')
        self.assertIsInstance(result, str)

    def test_returns_different_value(self):
        """The typo'd value should differ from the original."""
        original = 'IT12345678901'
        result = inject_typo(original)
        self.assertNotEqual(result, original)

    def test_preserves_country_prefix(self):
        """The first 2 chars (country prefix) should never change."""
        for prefix in ['IT', 'DE', 'FR', 'ES', 'GB']:
            value = prefix + '12345678901'
            result = inject_typo(value)
            self.assertTrue(result.startswith(prefix),
                            f"Prefix '{prefix}' not preserved: '{result}'")

    # ─── Length constraints ───
    def test_too_short_unchanged(self):
        """Values shorter than 4 chars should not be typo'd."""
        self.assertEqual(inject_typo(''), '')
        self.assertEqual(inject_typo('IT'), 'IT')
        self.assertEqual(inject_typo('IT1'), 'IT1')

    def test_min_length_works(self):
        """4-char values should be typo'd."""
        result = inject_typo('IT12')
        self.assertIsInstance(result, str)
        # Could be substitute (same length), delete (shorter), or insert (longer)
        # Just verify it's valid and prefix is preserved
        self.assertTrue(result.startswith('IT'))

    # ─── Typo types (run multiple times since type is random) ───
    def test_substitute_preserves_length(self):
        """Substitute typo should keep the same string length."""
        original = 'IT12345678901'
        for _ in range(50):
            result = inject_typo(original)
            if len(result) == len(original):
                # This was a substitute — prefix preserved, length same
                self.assertTrue(result.startswith('IT'))
                self.assertNotEqual(result, original)
                return
        # If we never got a substitute in 50 tries, something is wrong
        # (probability of no substitute in 50 tries ≈ (2/3)^50 ≈ 0.000000001)
        self.fail("Never got a substitute typo in 50 tries")

    def test_delete_reduces_length(self):
        """Delete typo should make the string shorter by 1 char."""
        original = 'IT12345678901'
        for _ in range(50):
            result = inject_typo(original)
            if len(result) == len(original) - 1:
                self.assertTrue(result.startswith('IT'))
                return
        self.fail("Never got a delete typo in 50 tries")

    def test_insert_increases_length(self):
        """Insert typo should make the string longer by 1 char."""
        original = 'IT12345678901'
        for _ in range(50):
            result = inject_typo(original)
            if len(result) == len(original) + 1:
                self.assertTrue(result.startswith('IT'))
                return
        self.fail("Never got an insert typo in 50 tries")

    # ─── Edge cases ───
    def test_none_input(self):
        """None input should return None (or empty, depending on implementation)."""
        result = inject_typo(None)
        # The function checks `if not value` — None is falsy, returns None
        self.assertIsNone(result)

    def test_alpha_value(self):
        """Alpha-heavy values (like Codice Fiscale) should work."""
        original = 'RSSMRA80A01H501Z'
        result = inject_typo(original)
        self.assertNotEqual(result, original)
        # First 2 chars preserved (even though for TIN they're not country prefix)
        self.assertTrue(result.startswith('RS'))

    def test_mixed_alphanumeric(self):
        """Mixed alphanumeric values (like IBAN) should work."""
        original = 'IT60X0538704481359716681436'
        result = inject_typo(original)
        self.assertNotEqual(result, original)
        self.assertTrue(result.startswith('IT'))

    def test_long_value(self):
        """Long values should work without issues."""
        original = 'IT' + '1' * 100
        result = inject_typo(original)
        self.assertNotEqual(result, original)
        self.assertTrue(result.startswith('IT'))

    # ─── Idempotency — each call should produce a (potentially) different typo ───
    def test_multiple_calls_produce_variety(self):
        """Multiple calls should produce different results (randomness works)."""
        original = 'IT12345678901'
        results = set()
        for _ in range(20):
            results.add(inject_typo(original))
        # With 3 typo types and ~10 possible positions, we should get
        # at least 2 different results in 20 calls
        self.assertGreater(len(results), 1)
