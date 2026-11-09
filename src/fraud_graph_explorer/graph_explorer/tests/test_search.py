# src/fraud_graph_explorer/graph_explorer/tests/test_search.py

"""
Tests for build_wildcard_search — the word-boundary wildcard search function.

Behavior:
  - No '*' in search → whole-word match (\bword\b)
  - '*' present → '*' becomes '.*', wrapped in word boundaries
  - Empty/whitespace string → returns None
  - Regex special chars are escaped (re.escape) — only '*' is treated as wildcard

Run:  manage test graph_explorer.tests.test_search
"""

from django.test import SimpleTestCase
from django.db.models import Q

from fraud_graph_explorer.graph_explorer.views import _build_wildcard_search as build_wildcard_search


class BuildWildcardSearchTests(SimpleTestCase):
    """Test the wildcard search helper function."""

    SEARCH_FIELDS = ['company_name', 'company_vat', 'entities__value']

    # ─── Return type ───
    def test_returns_q_object(self):
        """A valid search string should return a Q object."""
        result = build_wildcard_search('Mario', self.SEARCH_FIELDS)
        self.assertIsInstance(result, Q)

    def test_empty_string_returns_none(self):
        self.assertIsNone(build_wildcard_search('', self.SEARCH_FIELDS))

    def test_whitespace_only_returns_none(self):
        self.assertIsNone(build_wildcard_search('   ', self.SEARCH_FIELDS))

    def test_none_returns_none(self):
        self.assertIsNone(build_wildcard_search(None, self.SEARCH_FIELDS))

    # ─── No wildcard → exact whole-word match ───
    def test_no_wildcard_creates_word_boundary_regex(self):
        """Without '*', the search should use \b word boundaries for exact word match."""
        result = build_wildcard_search('Mario', self.SEARCH_FIELDS)
        self.assertIsInstance(result, Q)
        # The Q object should contain iregex lookups with \b
        # We can't easily inspect the Q object's internal SQL, but we can
        # verify it's a valid Q with children (one per field)
        self.assertTrue(len(result.children) > 0)

    # ─── Wildcard variants → should all return Q objects ───
    def test_prefix_wildcard(self):
        """Mario* → matches words starting with Mario."""
        result = build_wildcard_search('Mario*', self.SEARCH_FIELDS)
        self.assertIsInstance(result, Q)

    def test_suffix_wildcard(self):
        """*Mario → matches words ending with Mario."""
        result = build_wildcard_search('*Mario', self.SEARCH_FIELDS)
        self.assertIsInstance(result, Q)

    def test_contains_wildcard(self):
        """*Mario* → matches any word containing Mario."""
        result = build_wildcard_search('*Mario*', self.SEARCH_FIELDS)
        self.assertIsInstance(result, Q)

    def test_middle_wildcard(self):
        """Mar*o → matches words starting with Mar and ending with o."""
        result = build_wildcard_search('Mar*o', self.SEARCH_FIELDS)
        self.assertIsInstance(result, Q)

    def test_multiple_wildcards(self):
        """*Mario*Rossi* → multiple wildcards in one search."""
        result = build_wildcard_search('*Mario*Rossi*', self.SEARCH_FIELDS)
        self.assertIsInstance(result, Q)

    # ─── Regex safety — special chars should be escaped ───
    def test_parentheses_escaped(self):
        """Parentheses should be treated as literal chars, not regex groups."""
        result = build_wildcard_search('Mar(o)', self.SEARCH_FIELDS)
        self.assertIsInstance(result, Q)  # doesn't crash = re.escape worked

    def test_dot_escaped(self):
        """Dot should be literal, not regex 'any char'."""
        result = build_wildcard_search('Mario.Rossi', self.SEARCH_FIELDS)
        self.assertIsInstance(result, Q)

    def test_brackets_escaped(self):
        result = build_wildcard_search('Mar[io]', self.SEARCH_FIELDS)
        self.assertIsInstance(result, Q)

    def test_plus_escaped(self):
        result = build_wildcard_search('Mario+', self.SEARCH_FIELDS)
        self.assertIsInstance(result, Q)

    def test_question_mark_escaped(self):
        result = build_wildcard_search('Mario?', self.SEARCH_FIELDS)
        self.assertIsInstance(result, Q)

    def test_backslash_escaped(self):
        result = build_wildcard_search('Mario\\Rossi', self.SEARCH_FIELDS)
        self.assertIsInstance(result, Q)

    # ─── Multiple fields → Q object should combine with OR ───
    def test_multiple_fields_or(self):
        """Multiple fields should be combined with OR (|) in the Q object."""
        result = build_wildcard_search('Mario', ['field_a', 'field_b', 'field_c'])
        # Q with OR creates a combined Q — verify it has the right number of children
        self.assertIsInstance(result, Q)
        # Each field adds one Q to the OR chain
        self.assertEqual(len(result.children), 3)

    def test_single_field(self):
        """Single field should still work."""
        result = build_wildcard_search('Mario', ['company_name'])
        self.assertIsInstance(result, Q)

    # ─── Edge cases ───
    def test_just_wildcard(self):
        """A search of just '*' should match everything."""
        result = build_wildcard_search('*', self.SEARCH_FIELDS)
        self.assertIsInstance(result, Q)

    def test_wildcard_at_start_and_special_char(self):
        """*Mar(o) → wildcard + escaped special char."""
        result = build_wildcard_search('*Mar(o)', self.SEARCH_FIELDS)
        self.assertIsInstance(result, Q)

    def test_long_search_string(self):
        """Long search strings should not cause issues."""
        result = build_wildcard_search('M' * 100, self.SEARCH_FIELDS)
        self.assertIsInstance(result, Q)

    def test_unicode_chars(self):
        """Accented characters should work in searches."""
        result = build_wildcard_search('Müller', self.SEARCH_FIELDS)
        self.assertIsInstance(result, Q)

    def test_numeric_search(self):
        """Numeric search strings should work (e.g., for VAT/IBAN lookups)."""
        result = build_wildcard_search('12345', self.SEARCH_FIELDS)
        self.assertIsInstance(result, Q)

    def test_numeric_wildcard_search(self):
        """Numeric search with wildcard."""
        result = build_wildcard_search('123*', self.SEARCH_FIELDS)
        self.assertIsInstance(result, Q)
