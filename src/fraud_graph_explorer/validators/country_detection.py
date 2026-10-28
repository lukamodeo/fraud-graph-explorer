# src/fraud_graph_explorer/validators/country_detection.py

"""
Country-detection helpers for VAT and TIN identifiers.

These functions take an identifier value (VAT or TIN) and return the
ISO 3166-1 alpha-2 country code of the country whose format the value
matches, or None if no country's validator accepts it.

Used by:
- graph_explorer.validation_engine   — to decide "valid in any of 5 countries"
- graph_explorer.rules (future)      — to decide "is foreign to the sheet"
- graph_explorer.services.ingest_pdf — to populate Entity.country_code
- sheet_crafter.seed_gen             — to verify generated values

These functions are pure — no DB access, no side effects. They wrap the
lower-level stdnum/uk_nino validators with the country-detection layer.
"""

from stdnum import vatin as stdnum_vatin
from stdnum import iban as stdnum_iban
from stdnum.it import codicefiscale as it_tin
from stdnum.de import idnr as de_tin
from stdnum.fr import nir as fr_tin
from stdnum.es import dni as es_tin

from fraud_graph_explorer.validators.uk_nino import nino as gb_tin


# The 5 EU countries this PoC targets
TARGET_COUNTRIES = frozenset({'IT', 'DE', 'FR', 'ES', 'GB'})

# Dispatch table for TIN validators — canonical source of truth.
# Other modules (validation_engine.TIN_VALIDATORS, seed_gen.SEED_TIN_VALIDATORS)
# should import from here rather than re-defining the dict, so the validator
# mapping stays in one place.
TIN_VALIDATORS = {
    'IT': it_tin,
    'FR': fr_tin,
    'DE': de_tin,
    'ES': es_tin,
    'GB': gb_tin,
}


def detect_tin_country(value):
    """
    Return the ISO country code of the country whose TIN format matches
    `value`, or None if no country accepts it.

    Because the 5 target countries have distinct TIN formats (different
    lengths and character patterns — IT is 16 chars with letters,
    DE is 11 digits, FR is 13 digits, ES is 9 chars with letter suffix,
    GB is 9 chars with letters), at most one validator will ever pass.
    """
    if not value or not isinstance(value, str):
        return None

    for country_code, validator in TIN_VALIDATORS.items():
        try:
            if validator.is_valid(value):
                return country_code
        except Exception:
            # stdnum modules may raise on malformed input
            # (e.g., non-string, weird encoding); treat as "not valid"
            continue
    return None


def detect_vat_country(value):
    """
    Return the ISO country code of an EU VAT number, restricted to our
    5 target countries. Returns None if:
      - The value is not a valid EU VAT, OR
      - The value is a valid EU VAT but the country is outside our 5-country
        scope (e.g., 'NL123...' is valid in stdnum but not in our target set)

    Note: We extract the country code by reading the first 2 chars of the
    compacted value (the EU VAT format always starts with the ISO prefix)
    rather than calling vatin.get_country(), because that function is not
    available in all stdnum versions and uses a different error model.
    """
    if not value or not isinstance(value, str):
        return None

    try:
        if not stdnum_vatin.is_valid(value):
            return None
    except Exception:
        return None

    # VAT numbers always start with a 2-letter ISO country code
    # (per EU VAT format: 'IT12345678901', 'DE123456789', etc.)
    # Compact first (strip whitespace, uppercase) then slice.
    country = stdnum_vatin.compact(value)[:2].upper()
    if country not in TARGET_COUNTRIES:
        return None
    return country


def detect_iban_country(value):
    """
    Return the ISO 3166-1 alpha-2 country code of an IBAN, restricted to
    our 5 target countries (IT, DE, FR, ES, GB).

    Unlike TIN (where the country is inferred from the format), IBAN
    explicitly encodes the country in its first 2 characters. So detection
    is just: validate the full IBAN structure (including check digits),
    then read the country prefix.

    Returns None if:
      - The value is not a valid IBAN (fails check digits or structure), OR
      - The country prefix is outside our 5-country target set
        (e.g., 'NL...' is a valid IBAN but not in our scope)

    Examples:
        detect_iban_country('IT60X0542811101000000123456')  → 'IT'
        detect_iban_country('DE89370400440532013000')        → 'DE'
        detect_iban_country('FR1420041010050500013M02606')  → 'FR'
        detect_iban_country('ES9121000418450200051332')     → 'ES'
        detect_iban_country('GB29NWBK60161331926819')        → 'GB'
        detect_iban_country('NL91ABNA0417164300')            → None  (NL is valid EU, out of scope)
        detect_iban_country('not-an-iban')                   → None
        detect_iban_country('')                              → None
    """
    if not value or not isinstance(value, str):
        return None

    # Step 1: Validate the full IBAN structure
    # stdnum.iban.is_valid() checks:
    #   - Length per country (IBAN lengths are country-specific)
    #   - Mod-97 check digits
    #   - Country code is a known ISO code (any country, not just our 5)
    try:
        if not stdnum_iban.is_valid(value):
            return None
    except Exception:
        return None

    # Step 2: Extract the country code from the first 2 chars
    # The IBAN format is: [CC][DD][BBAN...]
    #   CC = 2-letter ISO country code
    #   DD = 2 check digits
    #   BBAN = country-specific Basic Bank Account Number
    # We can read the prefix directly — no need for a special stdnum function.
    country = value[:2].upper()

    # Step 3: Filter to our 5 target countries
    # (stdnum validates any IBAN, but we only care about IT/DE/FR/ES/GB)
    if country not in TARGET_COUNTRIES:
        return None

    return country