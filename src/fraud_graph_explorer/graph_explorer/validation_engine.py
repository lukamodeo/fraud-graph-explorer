# src/fraud_graph_explorer/graph_explorer/validation_engine.py

import ipaddress
import codicefiscale
from decimal import Decimal
from typing import Dict, Any, List, Callable
from collections import defaultdict
from stdnum import vatin, iban
from stdnum.it import codicefiscale as it_tin
from stdnum.de import idnr as de_tin
from stdnum.fr import nir as fr_tin
from stdnum.es import dni as es_tin
from stdnum.gb import utr as gb_tin
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from fraud_graph_explorer.domain_schema import split_italian_full_name


class Registry:
    def __init__(self, id_field_name: str):
        self.items: Dict[str, Dict[str, Any]] = {}
        self.id_field_name = id_field_name

    def register(self, item_id: str, reason_key: str = "", type_key: str = "generic", severity: str = "info", active: bool = True, scope: str = "field"):
        def decorator(fn: Callable):
            self.items[item_id] = {
                "fn": fn,
                "reason_key": reason_key,
                "type_key": type_key,
                "severity": severity,
                "active": active,
                "scope": scope
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
                    "type_key": r.get("type_key_override", meta.get("type_key")),
                    "reason_key": meta.get("reason_key"),
                    "severity": meta.get("severity"),
                    "value": val,
                    "raw_value": raw_val,
                    # FIX: Fallback to kwargs.get("internal_name")
                    "field": r.get("field", kwargs.get("internal_name")),
                    self.id_field_name: item_id
                })

        except Exception as e:
            results.append({
                "type_key": "TYPE_SYSTEM",
                "reason_key": f"Error executing '{item_id}': {str(e)}",
                "severity": "critical",
                "value": norm_value,
                "raw_value": raw_value,
                "field": kwargs.get("internal_name"),
                self.id_field_name: item_id
            })

        return results

    def get_meta(self, item_id: str) -> dict:
        return self.items.get(item_id, {})

# Instantiate ValidationRegistry
ValidationRegistry = Registry(id_field_name="validation_id")
RuleRegistry = Registry(id_field_name="rule_id")

# Map Country Codes to their specific stdnum TIN validators
TIN_VALIDATORS = {
    'IT': it_tin,
    'FR': fr_tin,
    'DE': de_tin,
    'ES': es_tin,
    'GB': gb_tin
}

# ==========================================
# VALIDATIONS (Validation Errors)
# ==========================================
@ValidationRegistry.register(
    item_id="email",
    type_key="TYPE_EMAIL",
    reason_key="REASON_EMAIL_INVALID",
    severity="critical",
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
    severity="critical",
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
    severity="critical",
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
    item_id="vat",
    type_key="TYPE_VAT",
    reason_key="REASON_VAT_INVALID",
    severity="critical",
    active=True
)
def check_vat(raw_value, norm_value, config, all_data, **kwargs):
    if norm_value and not vatin.is_valid(norm_value):
        return [{
            "value": norm_value,
            "raw_value": raw_value
        }]

    return []


@ValidationRegistry.register(
    item_id="iban",
    type_key="TYPE_IBAN",
    reason_key="REASON_IBAN_INVALID",
    severity="critical",
    active=True
)
def check_iban(raw_value, norm_value, config, all_data, **kwargs):
    if norm_value and not iban.is_valid(norm_value):
        return [{
            "value": norm_value,
            "raw_value": raw_value
        }]

    return []


@ValidationRegistry.register(
    item_id="tin",
    type_key="TYPE_TIN",
    reason_key="REASON_TIN_INVALID",
    severity="critical",
    active=True
)
def check_tin(raw_value, norm_value, config, all_data, **kwargs):
    """Validates TIN using the correct country-specific stdnum module."""
    if not norm_value:
        return []

    # Extract country_code from kwargs (passed by services.py)
    country_code = kwargs.get("country_code")
    validator = TIN_VALIDATORS.get(country_code.upper())

    if validator and not validator.is_valid(norm_value):
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
    severity="warning",
    scope="sheet",
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
                for field, raw_val in collisions:
                    warnings.append({
                        "value": norm_val,
                        "raw_value": raw_val,
                        "field": field,
                        "type_key_override": f"TYPE_DUPLICATE_{tag.upper()}"
                    })

    return warnings


@RuleRegistry.register(
    item_id="blacklist",
    type_key="TYPE_BLACKLIST",
    reason_key="REASON_IN_BLACKLIST",
    severity="critical",
    scope="field",
    active=True
)
def rule_blacklist_check(raw_value, norm_value, config, all_data, **kwargs):
    """
    Checks blacklists. Infers the specific blacklist type from the field's tags.
    """
    warnings = []
    blacklists = kwargs.get("blacklists", {})
    tags = config.get("tags", [])

    # Determine which blacklist to use based on tags
    bl_type = None
    if "VAT" in tags:
        bl_type = "vat"
    elif "TIN" in tags:
        bl_type = "tin"
    elif "IBAN" in tags:
        bl_type = "iban"
    elif "IP" in tags:
        bl_type = "ip"


    if not bl_type:
        return []

    bl_set = blacklists.get(bl_type, set())

    # Check if the normalized value is in the set
    if norm_value in bl_set:
        warnings.append({
            "value": norm_value,
            "raw_value": raw_value,
            # Removed "field": config["internal_name"] so Registry defaults it automatically
            "type_key_override": f"TYPE_BLACKLIST_{bl_type.upper()}"
        })

    return warnings


@RuleRegistry.register(
    item_id="positive",
    type_key="TYPE_POSITIVE",
    reason_key="REASON_POSITIVE_INVALID",
    severity="warning",
    scope="field",
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
    item_id="tin_name_check",
    type_key="TYPE_TIN_NAME_MISMATCH",
    reason_key="REASON_TIN_NAME_MISMATCH",
    severity="critical",
    scope="field",
    active=True
)
def rule_tin_name_check(raw_value, norm_value, config, all_data, **kwargs):
    """
    Crossing check (IT only): Verifies that the first 6 chars of the TIN
    mathematically match the provided Full Name.
    """
    warnings = []
    country_code = kwargs.get("country_code")

    # Only run for Italy
    if country_code != 'IT':
        return []

    # Find the related fullname field using the calc_fields map
    calc_fields = config.get("calc_fields", {})
    fullname_field = calc_fields.get("fullname")

    if not fullname_field:
        return []

    fullname = all_data.get(fullname_field, "")

    # 3. If either value is missing, skip (required_implicit handles empty fields)
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
            })

    except Exception:
        # If name splitting or CF generation fails, fail silently.
        # The 'tin' validation will catch malformed TINs.
        pass

    return warnings