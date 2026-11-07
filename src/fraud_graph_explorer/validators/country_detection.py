# src/fraud_graph_explorer/validators/country_detection.py

# Fraud Graph Explorer
# Copyright (C) 2026 Luca Amodeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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

import re

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


def _compact(value):
    """Lightweight compact: strip whitespace and dashes, uppercase."""
    return re.sub(r'[\s-]', '', value).upper()

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
            if validator.is_valid(_compact(value)):
                return country_code
        except Exception:
            # stdnum modules may raise on malformed input
            # (e.g., non-string, weird encoding); treat as "not valid"
            continue
    return None


def detect_vat_country(value):
    """
    Returns the ISO country code if the value's prefix matches one of our
    5 target countries — regardless of checksum validity.

    Returns None if:
    - The value is too short or has no alpha prefix
    - The prefix is outside our 5-country set (e.g., NL, AT, BE)

    This ensures Entity.country_code only contains supported codes,
    so flag/translation lookups never fail with KeyError.
    The checksum is NOT checked here — that's is_valid_vat()'s job.

    Note: We extract the country code by reading the first 2 chars of the
    compacted value (the EU VAT format always starts with the ISO prefix)
    rather than calling vatin.get_country(), because that function is not
    available in all stdnum versions and uses a different error model.
    """
    if not value or not isinstance(value, str) or len(value) < 2:
        return None

    # VAT numbers always start with a 2-letter ISO country code
    # (per EU VAT format: 'IT12345678901', 'DE123456789', etc.)
    # Compact first (strip whitespace, uppercase) then slice.
    country = _compact(value)[:2]

    if country not in TARGET_COUNTRIES:
        return None

    return country


def detect_iban_country(value):
    """
    Returns the ISO country code if the value's prefix matches one of our
    5 target countries — regardless of checksum validity.

    Returns None if:
    - The value is too short or has no alpha prefix
    - The prefix is outside our 5-country set (e.g., NL, AT, BE)

    This ensures Entity.country_code only contains supported codes,
    so flag/translation lookups never fail with KeyError.
    The checksum is NOT checked here — that's is_valid_vat()'s job.

    Unlike TIN (where the country is inferred from the format), IBAN
    explicitly encodes the country in its first 2 characters. So detection
    is just: read the country prefix.
    """
    if not value or not isinstance(value, str) or len(value) < 2:
        return None


    # The IBAN format is: [CC][DD][BBAN...]
    #   CC = 2-letter ISO country code
    #   DD = 2 check digits
    #   BBAN = country-specific Basic Bank Account Number
    # We can read the prefix directly — no need for a special stdnum function.
    country = _compact(value)[:2]

    if country not in TARGET_COUNTRIES:
        return None

    return country