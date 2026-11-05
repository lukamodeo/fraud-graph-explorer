# src/fraud_graph_explorer/graph_explorer/alerts.py

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

from typing import Literal

from fraud_graph_explorer.domain_schema import FIELDS, SECTION_BY_FIELD

def _localized_lookup(ui_strings, key, type_country, country_code, fallback=None):
    """
    Look up `key` in `ui_strings`, transparently handling both:
      - Regular 2D entries (already flattened to a string by get_ui_strings)
      - "ANY"-wrapped entries (kept as {country_code: string} sub-dict)

    Fallback chain (only applies when value is a dict):
      1. type_country  (alert's identifier_country — the "sub_dict" lookup)
      2. country_code (sheet's country — the "flatten" fallback, what
                       get_ui_strings would have picked if no "ANY" wrapper)
      3. 'GB'         (last resort for missing translations)
      4. fallback     (defaults to the key itself, so missing translations
                       are visible in the rendered output)

    For regular 2D entries (string value), the value is returned as-is —
    no fallback chain needed because get_ui_strings already did the lookup.
    """
    if fallback is None:
        fallback = key

    value = ui_strings.get(key, fallback)

    if isinstance(value, dict):
        # "ANY"-wrapped entry — country-aware lookup with fallbacks
        return (
            value.get(type_country)     # 1. sub_dict: alert's identifier_country
            or value.get(country_code)  # 2. flatten: sheet's country
            or value.get('GB')          # 3. GB fallback
            or fallback                 # 4. key itself
        )
    # Regular 2D entry — already flattened by get_ui_strings
    return value


def resolve_alerts(alerts_list, ui_strings, country_code, alert_type: Literal["error", "warning"]):
    """
    Convert raw error/warning dicts (from JSONField) into presentation-ready dicts.

    Args:
        alerts_list: list of raw alert dicts (from app.validation_errors
                     or app.rule_warnings JSONField).
        ui_strings: dict of UI translations (from get_ui_strings()).
                     May contain regular 2D entries (strings) OR "ANY"-wrapped
                     entries ({country_code: string} dicts) — _localized_lookup
                     handles both transparently.
        country_code: SHEET's 2-letter ISO code (used for section/field labels
                      AND as the "flatten" fallback for any "ANY"-wrapped entry
                      whose type_country lookup fails).
        alert_type: 'error' or 'warning' — distinguishes the source list.

    Each output item:
        {
            'alert_bs_color':    'danger' | 'warning',
            'severity':          'high' | 'medium' | 'low',
            'severity_class':    str (e.g., 'severity-error-high'),
            'level_tooltip':     str (e.g., 'Livello: Alto'),
            'type_label':       str (translated, country-aware via "ANY" wrapper),
            'reason_label':     str (translated, country-aware if "ANY"-wrapped),
            'raw_value':          str,
            'section_label':      str (sheet's country language),
            'field_label':        str (sheet's country language),
            'field_name':         str (internal_name, e.g., 'representative_tin'),
            'identifier_country': str (e.g., 'GB' for foreign_identifier; empty otherwise),
            'count':              int (default 1; >1 only for duplicate rule),
            'icon':                str (Bootstrap Icon class, e.g., 'bi-shield-slash'),
        }
    Missing translation keys fall back to the key itself so you can spot gaps.
    """
    resolved = []
    for alert in alerts_list or []:
        field_name = alert.get('field', '')

        # --- Determine which country to use for "ANY"-wrapped lookups ---
        # alert's identifier_country if set, else None (the lookup helper
        # will fall back to country_code = sheet's country).
        identifier_country = alert.get('identifier_country', '')
        type_country = identifier_country or None
        # NOTE: passing None (not '') to _localized_lookup so the first
        # .get(None) returns None and naturally falls through to the
        # country_code fallback. If we passed '', .get('') would also
        # return None for missing keys, but None is more explicit.

        # --- Section + field label lookups (use SHEET's country directly) ---
        # These are NOT "ANY"-wrapped — they always use the sheet's country
        # because sections/fields are part of the sheet's structure.
        section_dict = SECTION_BY_FIELD.get(field_name)
        section_labels = section_dict.get('labels', {}) if section_dict else {}
        section_label = section_labels.get(country_code, '') if section_dict else ''

        # Field label lookup: 'labels' dict indexed by country
        field_config = FIELDS.get(field_name, {})
        field_labels = field_config.get('labels', {})
        field_label = field_labels.get(country_code, field_name)

        # --- Type and reason: use _localized_lookup (handles "ANY" wrapper) ---
        # If the key is "ANY"-wrapped (e.g., TYPE_BLACKLIST_VAT), the lookup
        # uses type_country ? country_code ? GB ? key.
        # If the key is a regular 2D entry, the value is a string (already
        # flattened) and is returned as-is.
        type_key = alert.get('type_key', '')
        type_label = _localized_lookup(ui_strings, type_key, type_country, country_code)

        reason_key = alert.get('reason_key', '')
        reason_label = _localized_lookup(ui_strings, reason_key, type_country, country_code)

        # --- Severity + level_tooltip (use _localized_lookup for consistency) ---
        # If you ever wrap SEVERITY_HIGH or SEVERITY_LEVEL_LABEL in "ANY",
        # the lookup still works.
        severity = alert.get('severity', 'medium')
        severity_label_key = f"SEVERITY_{severity.upper()}"  # e.g., SEVERITY_HIGH
        severity_label = _localized_lookup(ui_strings, severity_label_key, type_country, country_code)
        level_label = _localized_lookup(ui_strings, 'SEVERITY_LEVEL_LABEL', type_country, country_code, fallback='Level')
        level_tooltip = f"{level_label}: {severity_label}"  # e.g., "Livello: Alto"

        resolved.append({
            # Bootstrap color class for the badge (danger for errors, warning for warnings)
            "alert_bs_color":   "warning" if alert_type == "warning" else "danger",
            # CSS class for severity gradient (e.g., severity-error-high)
            "severity_class": f"severity-{alert_type}-{severity}",
            "severity":         severity,
            "level_tooltip":    level_tooltip,
            "type_label":       type_label,
            "reason_label":     reason_label,
            "raw_value":        alert.get("raw_value", alert.get("value", "")),
            "section_label":    section_label,
            "field_label":      field_label,
            "field_name":       field_name,
            "identifier_country": identifier_country,
            "count":            alert.get("count", 1),
            "icon":             alert.get("icon", "bi-exclamation-circle"),
        })
    return resolved


