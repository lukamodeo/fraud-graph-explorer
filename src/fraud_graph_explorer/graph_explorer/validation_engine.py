# src/fraud_graph_explorer/graph_explorer/validation_engine.py

import ipaddress
import codicefiscale
from decimal import Decimal
from typing import Dict, Any, List, Callable, Literal
from collections import defaultdict

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from fraud_graph_explorer.domain_schema import split_italian_full_name
# Use the shared country-detection helpers — they encapsulate "try all 5
# validators, return the country code of whichever one passes (or None)".
# The validation function's pass/fail decision is just "is the detected
# country not None?". The detected country is also available for the
# foreign_identifier rule (Step 5) to compare against the sheet's country.
from fraud_graph_explorer.validators.country_detection import detect_tin_country, detect_vat_country, detect_iban_country


class Registry:
    def __init__(self, id_field_name: str):
        self.items: Dict[str, Dict[str, Any]] = {}
        self.id_field_name = id_field_name

    def register(self, item_id: str, reason_key: str = "", type_key: str = "generic", severity: Literal['high', 'medium', 'low'] = 'medium', scope: str = "field", icon: str = "bi-exclamation-circle", active: bool = True ):
        def decorator(fn: Callable):
            self.items[item_id] = {
                "fn": fn,
                "reason_key": reason_key,
                "type_key": type_key,
                "severity": severity,
                "active": active,
                "scope": scope,
                "icon": icon,
                }
            return fn

        return decorator

    # Removed rule_name parameter. item_id is used for both lookup and JSON output.
    def run(self, item_id: str, raw_value: str, norm_value: str, config: dict, all_data: dict, **kwargs) -> List[Dict[str, Any]]:
        meta = self.items.get(item_id)
        if not meta or not meta.get("active", True):
            return []

        fn = meta["fn"]
        results = []
        try:
            # Pass both raw and normalized values
            fn_results = fn(raw_value, norm_value, config, all_data, **kwargs)
            for r in fn_results:

                # FIX 4: Ensure Decimal objects are JSON serializable
                val = r.get("value", norm_value)
                raw_val = r.get("raw_value", raw_value)
                if isinstance(val, Decimal):
                    val = str(val) # Convert -100.00 to "-100.00"
                if isinstance(raw_val, Decimal):
                    raw_val = str(raw_val)

                results.append({
                    "type_key":   r.get("type_key_override") or meta["type_key"],
                    "reason_key": r.get("reason_key_override") or meta["reason_key"],
                    "severity":   meta["severity"],
                    "value":      val,
                    "raw_value":  raw_val,
                    "field":      r.get("field", kwargs.get("internal_name")),
                    self.id_field_name: item_id,
                    # ─── Forwarded payload fields (added incrementally) ───
                    # identifier_country: set by foreign_identifier rule only
                    # count:               set by duplicate rule only (defaults to 1)
                    # icon:                declared on the @register decorator
                    "identifier_country": r.get("identifier_country", ""),
                    "count": r.get("count", 1),
                    "icon":  meta["icon"],
                })

        except Exception as e:
            results.append({
                "type_key":   "TYPE_SYSTEM",
                "reason_key": f"Error executing '{item_id}': {str(e)}",
                "severity":   "critical",
                "value":      norm_value,
                "raw_value":  raw_value,
                "field":      kwargs.get("internal_name"),
                self.id_field_name: item_id,
                # Keep the result shape consistent between success and error branches.
                # count defaults to 1 (not 0) so the template's `{% if alert.count > 1 %}`
                # condition doesn't accidentally fire on error-branch results.
                # icon uses 'bi-bug' to make system errors visually distinct.
                "identifier_country": "",
                "count": 1,
                "icon": "bi-bug",
            })

        return results

    def get_meta(self, item_id: str) -> dict:
        return self.items.get(item_id, {})

# Instantiate ValidationRegistry
ValidationRegistry = Registry(id_field_name="validation_id")
RuleRegistry = Registry(id_field_name="rule_id")


# ==========================================
# VALIDATIONS (Validation Errors)
# ==========================================
@ValidationRegistry.register(
    item_id="email",
    type_key="TYPE_EMAIL",
    reason_key="REASON_EMAIL_INVALID",
    severity="high",
    icon="bi-envelope-at",
    active=True
)
def check_email(raw_value, norm_value, config, all_data, **kwargs):
    """Checks if a value is a valid email address using Django's built-in validator."""
    # If empty, let the 'required' check handle it
    if not raw_value:
        return []

    try:
        # We validate the normalized value (which is already lowercased and stripped)
        validate_email(norm_value)
    except ValidationError:
        return [{
            "value": norm_value,
            "raw_value": raw_value
        }]

    return []

@ValidationRegistry.register(
    item_id="ip",
    type_key="TYPE_IP",
    reason_key="REASON_IP_INVALID",
    severity="medium",
    icon="bi-globe2",
    active=True
)
def check_ip(raw_value, norm_value, config, all_data, **kwargs):
    """Checks if a value is a valid IPv4 address."""
    if not raw_value:
        return []

    try:
        # We validate the RAW value, because norm_value is already padded
        ipaddress.IPv4Address(raw_value)
    except ipaddress.AddressValueError:
        return [{
            "value": raw_value,
            "raw_value": raw_value
        }]

    return []

@ValidationRegistry.register(
    item_id="numeric",
    type_key="TYPE_NUMERIC",
    reason_key="REASON_NUMERIC_INVALID",
    severity="low",
    icon="bi-calculator",
    active=True
)
def check_numeric(raw_value, norm_value, config, all_data, **kwargs):
    """Checks if a value meant to be a number was successfully parsed as a Decimal."""
    # If the field is empty, it's not a numeric error (required_implicit handles empty fields)
    if not raw_value:
        return []

    # If norm_value is not a Decimal (or int/float), it means the conversion in services.py failed
    if not isinstance(norm_value, (Decimal, int, float)):
        return [{
            "value": raw_value,
            "raw_value": raw_value
        }]

    return []

@ValidationRegistry.register(
    item_id="iban",
    type_key="TYPE_IBAN",
    reason_key="REASON_IBAN_INVALID",
    severity="high",
    icon="bi-bank",
    active=True
)
def check_iban(raw_value, norm_value, config, all_data, **kwargs):
    """
    Validates IBAN — restricted to our 5 target countries.

    detect_iban_country() returns None if either:
      - the value is not a valid IBAN (fails checksum), OR
      - the value is a valid IBAN but the country prefix is outside
        our 5-country target set (e.g., 'NL91...', 'BE68...')

    Both cases produce one REASON_IBAN_INVALID error.

    identifier_country is extracted from the first 2 chars so the alert's
    type_label reflects the intended country — e.g., 'ES000000' on an IT
    sheet shows "Spanish IBAN invalid", not "Italian IBAN invalid".
    """
    if not norm_value:
        return []

    if detect_iban_country(norm_value) is None:
        identifier_country = norm_value[:2].upper() if len(norm_value) >= 2 else ''
        return [{
            "value": norm_value,
            "raw_value": raw_value,
            "identifier_country": identifier_country,
        }]

    return []

@ValidationRegistry.register(
    item_id="vat",
    type_key="TYPE_VAT",
    reason_key="REASON_VAT_INVALID",
    severity="high",
    icon="bi-credit-card-2-front",
    active=True
)
def check_vat(raw_value, norm_value, config, all_data, **kwargs):
    """
    Validates VAT — restricted to our 5 target countries.

    detect_vat_country() returns None if either:
      - the value is not a valid EU VAT (fails vatin.is_valid), OR
      - the value is a valid EU VAT but the country prefix is outside
        our 5-country target set (e.g., 'NL123...', 'AT123...')

    Both cases produce one REASON_VAT_INVALID error.

    identifier_country is extracted from the first 2 chars so the alert's
    type_label reflects the intended country.
    """
    if not norm_value:
        return []

    if detect_vat_country(norm_value) is None:
        identifier_country = norm_value[:2].upper() if len(norm_value) >= 2 else ''
        return [{
            "value": norm_value,
            "raw_value": raw_value,
            "identifier_country": identifier_country,
        }]

    return []

@ValidationRegistry.register(
    item_id="tin",
    type_key="TYPE_TIN",
    reason_key="REASON_TIN_INVALID",
    severity="high",
    icon="bi-person-vcard",
    active=True
)
def check_tin(raw_value, norm_value, config, all_data, **kwargs):
    """
    Validates TIN against all 5 target countries via detect_tin_country().

    The value is valid if it matches the format of ANY of IT/DE/FR/ES/GB.
    The sheet's own country is no longer used for the validation decision
    (any country's format is accepted). The sheet's country_code kwarg is
    still passed in for the rule layer (Step 5) to detect "foreign
    identifier" warnings — but this function doesn't use it.
    """
    if not norm_value:
        return []

    # detect_tin_country() returns the ISO code of whichever country's
    # validator passes, or None if none of the 5 accept the value.
    # That single None-check IS the validation.
    if detect_tin_country(norm_value) is None:
        return [{
            "value": norm_value,
            "raw_value": raw_value
        }]

    return []


# ==========================================
# RULES (Rule Warnings - Dynamic & Tag-Driven)
# ==========================================

# scope="sheet" means it runs ONCE per PDF

def _extract_values_for_rule(all_data: dict, schema: dict, rule_name: str) -> dict:
    """
    Dynamically extracts all single values for fields containing the specified rule.
    """
    values = defaultdict(list)

    for internal_name, config in schema.get("FIELDS", {}).items():
        if rule_name not in config.get("rules", []):
            continue

        val = all_data.get(internal_name)
        if not val:
            continue

        values[internal_name].append(val)

    return values

@RuleRegistry.register(
    item_id="duplicate",
    type_key="TYPE_DUPLICATE",
    reason_key="REASON_DUPLICATE_VALUE",
    severity="low",
    scope="sheet",
    icon="bi-files",
    active=True
)
def rule_duplicate_value_check(raw_value, norm_value, config, all_data, **kwargs):
    """
    Detects duplicated values across fields that share the same graph tag (e.g., TIN vs TIN).
    Runs once per sheet.
    """
    warnings = []
    schema_fields = kwargs.get("schema", {}).get("FIELDS", {})
    raw_data = kwargs.get("raw_data", {}) # <-- GET THE RAW DATA DICT

    # Group all normalized values by their graph tag, carrying the raw_value with them
    values_by_tag = defaultdict(list)

    for internal_name, norm_val in all_data.items():
        f_config = schema_fields.get(internal_name, {})
        if "duplicate" not in f_config.get("rules", []):
            continue

        for tag in f_config.get("tags", []):
            if tag != "Sheet":
                # Look up the forensic raw value for this specific field
                raw_val = raw_data.get(internal_name, norm_val)
                # Store tuple: (field_name, norm_val, raw_val)
                values_by_tag[tag].append((internal_name, norm_val, raw_val))

    # Check for duplicates within each tag group
    for tag, items in values_by_tag.items():
        reverse = defaultdict(list)
        for field, norm_val, raw_val in items:
            reverse[norm_val].append((field, raw_val))

        # If a value appears in 2+ fields, generate a warning for each field
        for norm_val, collisions in reverse.items():
            if len(collisions) > 1:
                # NEW: detect identifier country for VAT/TIN tags
                if tag == "VAT":
                    detected_country_code = detect_vat_country(norm_val) or ""
                elif tag == "TIN":
                    detected_country_code = detect_tin_country(norm_val) or ""
                elif tag == "IBAN":
                    detected_country_code = detect_iban_country(norm_val) or ""
                else:
                    detected_country_code = ""   # FULLNAME, IP, etc. don't have country detection

                for field, raw_val in collisions:
                    warnings.append({
                        "value": norm_val,
                        "raw_value": raw_val,
                        "field": field,
                        "count": len(collisions),
                        "type_key_override": f"TYPE_DUPLICATE_{tag.upper()}",
                        "identifier_country": detected_country_code,
                    })

    return warnings


@RuleRegistry.register(
    item_id="blacklist",
    type_key="TYPE_BLACKLIST",
    reason_key="REASON_IN_BLACKLIST",
    severity="high",
    scope="field",
    icon="bi-shield-slash",
    active=True
)
def rule_blacklist_check(raw_value, norm_value, config, all_data, **kwargs):
    """
    Checks blacklists. Infers the specific blacklist type from the field's tags.
    Also detects the identifier's country (for VAT/TIN) so the resolver can
    translate type_label using the IDENTIFIER's country context (e.g.,
    "French TVA Blacklist" instead of "Italian P.IVA Blacklist" when a French
    VAT appears on an Italian sheet).
    """
    warnings = []
    blacklists = kwargs.get("blacklists", {})
    tags = config.get("tags", [])

    # Determine which blacklist to use based on tags + detect identifier country
    bl_type = None
    detected_country_code = None
    if "VAT" in tags:
        bl_type = "vat"
        detected_country_code = detect_vat_country(norm_value)
    elif "TIN" in tags:
        bl_type = "tin"
        detected_country_code = detect_tin_country(norm_value)
    elif "IBAN" in tags:
        bl_type = "iban"
        detected_country_code = detect_iban_country(norm_value)
    elif "IP" in tags:
        bl_type = "ip"
        # IP doesn't have country detection — leave as None

    if not bl_type:
        return []

    bl_set = blacklists.get(bl_type, set())

    # Check if the normalized value is in the set
    if norm_value in bl_set:
        warnings.append({
            "value": norm_value,
            "raw_value": raw_value,
            "type_key_override": f"TYPE_BLACKLIST_{bl_type.upper()}",
            "identifier_country": detected_country_code or "",
        })

    return warnings


@RuleRegistry.register(
    item_id="positive",
    type_key="TYPE_POSITIVE",
    reason_key="REASON_POSITIVE_INVALID",
    severity="medium",
    scope="field",
    icon="bi-dash-circle",
    active=True
)
def rule_positive(raw_value, norm_value, config, all_data, **kwargs):
    """Checks if a numeric value is strictly greater than zero."""
    # Only run this rule if the value was successfully parsed as a number
    if isinstance(norm_value, (Decimal, int, float)):
        if norm_value <= 0:
            return [{
                "value": norm_value,
                "raw_value": raw_value
            }]

    return []


@RuleRegistry.register(
    item_id="foreign_identifier",
    type_key="TYPE_FOREIGN",            # default — overridden per identifier type
    reason_key="REASON_FOREIGN_IDENTIFIER",
    severity="low",
    scope="field",
    icon="bi-flag",
    active=True
)
def rule_foreign_identifier(raw_value, norm_value, config, all_data, **kwargs):
    """
    Warn when an identifier is valid in a country OTHER than the sheet's
    own country. Cross-border identifier — could be legitimate (e.g., a
    British guarantor on an Italian sheet) but worth flagging for review.

    The validation engine (Step 4) already accepted the value as valid
    for some country; this rule emits a warning when that country
    differs from the sheet's country.

    Applies to fields with VAT, TIN, or IBAN in their tags. Other identifier
    types (FULLNAME, IP, EMAIL, PHONE, COMPANY, LOCATION) don't have
    country-aware formats, so the "foreign" concept doesn't apply.

    Payload (added to each warning dict):
      - value:              normalized value
      - raw_value:          original PDF value
      - type_key_override:  'TYPE_FOREIGN_VAT', 'TYPE_FOREIGN_TIN', or 'TYPE_FOREIGN_IBAN'
      - reason_key_override: 'REASON_FOREIGN_VAT', 'REASON_FOREIGN_TIN', or 'REASON_FOREIGN_IBAN'
      - identifier_country: ISO code of the detected foreign country
    """
    if not norm_value:
        return []

    tags = config.get("tags", [])
    sheet_country = kwargs.get("country_code")

    # Determine which detector to use based on the field's tags
    if "VAT" in tags:
        detected = detect_vat_country(norm_value)
        identifier_type = "VAT"
    elif "TIN" in tags:
        detected = detect_tin_country(norm_value)
        identifier_type = "TIN"
    elif "IBAN" in tags:
        detected = detect_iban_country(norm_value)
        identifier_type = "IBAN"
    else:
        # Not an identifier type we country-detect
        return []

    # If validation failed (detected is None), the validation engine
    # already emitted a critical error — don't double-report here.
    if detected is None:
        return []

    # Same country as the sheet → no warning (the normal case)
    if detected == sheet_country:
        return []

    # Detected country is foreign to the sheet → emit warning
    return [{
        "value": norm_value,
        "raw_value": raw_value,
        "type_key_override": f"TYPE_FOREIGN_{identifier_type}",
        "reason_key_override": f"REASON_FOREIGN_{identifier_type}",
        "identifier_country": detected,
    }]


@RuleRegistry.register(
    item_id="tin_name_check",
    type_key="TYPE_TIN_NAME_MISMATCH",
    reason_key="REASON_TIN_NAME_MISMATCH",
    severity="medium",
    scope="field",
    icon="bi-person-slash",
    active=True
)
def rule_tin_name_check(raw_value, norm_value, config, all_data, **kwargs):
    """
    Crossing check (IT only): Verifies that the first 6 chars of the TIN
    mathematically match the provided Full Name.

    Uses detect_tin_country(norm_value) instead of the sheet's country_code,
    so the check correctly fires on Italian Codice Fiscale values that
    appear on ANY sheet (not just Italian sheets). This handles the
    cross-border case where an Italian guarantor on a British application
    has a Codice Fiscale that should match their name.
    """
    warnings = []

    # ─── NEW: Check the TIN's country (not the sheet's country) ───
    # The Codice Fiscale algorithm only applies to Italian TINs.
    # detect_tin_country() tries all 5 validators and returns the country
    # code of whichever one passes (or None if invalid for all 5).
    detected_country_code = detect_tin_country(norm_value)
    if detected_country_code != 'IT':
        return []   # not an Italian CF — CF name-mismatch check doesn't apply
    # ────────────────────────────────────────────────────────────────────

    # Find the related fullname field using the calc_fields map
    calc_fields = config.get("calc_fields", {})
    fullname_field = calc_fields.get("fullname")

    if not fullname_field:
        return []

    fullname = all_data.get(fullname_field, "")

    # If either value is missing, skip (required_implicit handles empty fields)
    if not fullname or not norm_value:
        return []

    try:
        # Split the name into First and Last
        first_name, last_name = split_italian_full_name(fullname)

        # Generate a dummy CF just to get the first 6 characters (Name + Surname code)
        # We use dummy data for DOB/Sex/Place because we ONLY care about the first 6 chars
        dummy_cf = codicefiscale.encode(
            lastname=last_name,
            firstname=first_name,
            gender="M",
            birthdate="1900-01-01",
            birthplace="H501"
        )

        # Compare the first 6 characters
        expected_prefix = dummy_cf[:6]
        actual_prefix = norm_value[:6]

        if expected_prefix != actual_prefix:
            warnings.append({
                "value": norm_value,
                "raw_value": raw_value,
                "identifier_country": detected_country_code,
            })

    except Exception:
        # If name splitting or CF generation fails, fail silently.
        # The 'tin' validation will catch malformed TINs.
        pass

    return warnings


if __name__ == "__main__":
    from fraud_graph_explorer.domain_schema import FIELDS

    # Assuming RuleRegistry is a singleton or has a classmethod to access the registry
    registry = RuleRegistry  # adjust to match your actual access pattern
    results = registry.run(
        item_id="foreign_identifier",
        raw_value="LJ551795A",
        norm_value="LJ551795A",
        config={
            **FIELDS["representative_tin"],
            "internal_name": "representative_tin"
            },
        all_data={},
        country_code="IT",
        internal_name="representative_tin",
        )

    assert len(results) == 1
    assert results[0]["identifier_country"] == "GB"
    assert results[0]["type_key"] == "TYPE_FOREIGN_TIN"
    assert results[0]["rule_id"] == "foreign_identifier"
    print(f"✓ Full run() pipeline preserves identifier_country: {results[0]}")