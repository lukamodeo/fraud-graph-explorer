# src/fraud_graph_explorer/graph_explorer/tests/test_country_detection.py

"""
Tests for the refactored detect_vat_country / detect_iban_country functions.

These functions return the 5-country ISO code if the value's prefix matches
one of our target countries (IT, DE, FR, ES, GB) — regardless of checksum
validity. Returns None for unsupported countries or unrecognizable prefixes.

Run:  manage test validators.tests.test_country_detection
"""

from django.test import SimpleTestCase

from fraud_graph_explorer.validators.country_detection import detect_vat_country, detect_iban_country

class DetectVatCountryTests(SimpleTestCase):
    """Test detect_vat_country — prefix-based country detection for VAT."""

    # ─── Supported country prefixes → returns the country code ───
    def test_italian_prefix(self):
        self.assertEqual(detect_vat_country('IT12345678901'), 'IT')

    def test_german_prefix(self):
        self.assertEqual(detect_vat_country('DE123456789'), 'DE')

    def test_french_prefix(self):
        self.assertEqual(detect_vat_country('FR12345678901'), 'FR')

    def test_spanish_prefix(self):
        self.assertEqual(detect_vat_country('ESB12345678'), 'ES')

    def test_british_prefix(self):
        self.assertEqual(detect_vat_country('GB123456789'), 'GB')

    # ─── Invalid checksum but supported prefix → still returns country ───
    # This is the key behavior of the refactor: detect_*_country does NOT
    # check the checksum. It only checks the prefix against the 5-country set.
    def test_invalid_italian_vat_still_returns_country(self):
        self.assertEqual(detect_vat_country('IT00000000000'), 'IT')

    def test_invalid_spanish_vat_still_returns_country(self):
        self.assertEqual(detect_vat_country('ES00000000'), 'ES')

    def test_invalid_french_vat_still_returns_country(self):
        self.assertEqual(detect_vat_country('FR00000000000'), 'FR')

    def test_invalid_german_vat_still_returns_country(self):
        self.assertEqual(detect_vat_country('DE000000000'), 'DE')

    def test_invalid_british_vat_still_returns_country(self):
        self.assertEqual(detect_vat_country('GB000000000'), 'GB')

    # ─── Unsupported country prefixes → returns None ───
    def test_dutch_vat_unsupported(self):
        self.assertIsNone(detect_vat_country('NL123456789B01'))

    def test_austrian_vat_unsupported(self):
        self.assertIsNone(detect_vat_country('ATU12345678'))

    def test_belgian_vat_unsupported(self):
        self.assertIsNone(detect_vat_country('BE0123456789'))

    def test_irish_vat_unsupported(self):
        self.assertIsNone(detect_vat_country('IE1234567FA'))

    # ─── Edge cases ───
    def test_empty_string(self):
        self.assertIsNone(detect_vat_country(''))

    def test_single_char(self):
        self.assertIsNone(detect_vat_country('I'))

    def test_none_input(self):
        self.assertIsNone(detect_vat_country(None))

    def test_numeric_prefix(self):
        """No alpha prefix → can't determine country."""
        self.assertIsNone(detect_vat_country('12345678901'))

    def test_whitespace_compaction(self):
        """Leading/trailing spaces and internal spaces should be handled."""
        self.assertEqual(detect_vat_country(' IT 12345678901 '), 'IT')

    def test_internal_spaces(self):
        """Internal spaces in the value should be removed before prefix check."""
        self.assertEqual(detect_vat_country('I T12345678901'), 'IT')

    def test_lowercase_prefix(self):
        """Lowercase prefix should be uppercased."""
        self.assertEqual(detect_vat_country('it12345678901'), 'IT')

    def test_mixed_case_prefix(self):
        self.assertEqual(detect_vat_country('It12345678901'), 'IT')

    def test_special_chars_only(self):
        """Non-alpha prefix → None."""
        self.assertIsNone(detect_vat_country('--12345678901'))


class DetectIbanCountryTests(SimpleTestCase):
    """Test detect_iban_country — same prefix-based logic, different identifier."""

    def test_italian_iban(self):
        self.assertEqual(detect_iban_country('IT60X0538704481359716681436'), 'IT')

    def test_german_iban(self):
        self.assertEqual(detect_iban_country('DE89370400440532013000'), 'DE')

    def test_french_iban(self):
        self.assertEqual(detect_iban_country('FR1420041010050500013M02606'), 'FR')

    def test_spanish_iban(self):
        self.assertEqual(detect_iban_country('ES9121000418450200051332'), 'ES')

    def test_british_iban(self):
        self.assertEqual(detect_iban_country('GB29NWBK60161331926819'), 'GB')

    def test_invalid_iban_supported_country(self):
        """Invalid checksum but supported prefix → still returns country."""
        self.assertEqual(detect_iban_country('IT00X0000000000000000000000'), 'IT')

    def test_dutch_iban_unsupported(self):
        self.assertIsNone(detect_iban_country('NL91ABNA0417164300'))

    def test_belgian_iban_unsupported(self):
        self.assertIsNone(detect_iban_country('BE68539007547034'))

    def test_empty_string(self):
        self.assertIsNone(detect_iban_country(''))

    def test_none_input(self):
        self.assertIsNone(detect_iban_country(None))

    def test_whitespace_compaction(self):
        self.assertEqual(detect_iban_country(' IT60 X0538 7044 '), 'IT')

    def test_lowercase_prefix(self):
        self.assertEqual(detect_iban_country('it60x0538704481359716681436'), 'IT')
