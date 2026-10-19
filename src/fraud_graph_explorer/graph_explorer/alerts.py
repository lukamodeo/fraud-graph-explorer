# src/fraud_graph_explorer/graph_explorer/alerts.py

from fraud_graph_explorer.domain_schema import FIELDS, SECTION_BY_FIELD


# Map the validation engine's severity vocab to Bootstrap contextual names
# so the template can use bg-{{ alert.severity }}-subtle
_SEVERITY_TO_BOOTSTRAP = {
    'critical': 'danger',
    'error':    'danger',
    'warning':  'warning',
    'info':     'info',
    'success':  'success',
}


def resolve_alerts(alerts_list, ui_strings, country_code):
    """
    Convert raw error/warning dicts (from JSONField) into presentation-ready dicts.

    Translation policy (2D):
      - type_label, reason_label  → ui_strings (BROWSER language)
      - section_label, field_label → schema 'labels' dict, indexed by SHEET country

    Each output item:
        {
            'severity': 'danger',                  # Bootstrap-friendly
            'type_label':     'TIN',                          # ui['TYPE_TIN']  (browser lang)
            'reason_label':   'Invalid TIN',                  # ui['REASON_TIN_INVALID'] (browser lang)
            'raw_value': 'CLMFNC80D15H501R',
            'section_label':  'DATI DEL LEGALE RAPPRESENTANTE', # sheet country (e.g. IT)
            'field_label':    'CODICE FISCALE',                 # sheet country (e.g. IT)
            'field_name':     'representative_tin',           # raw, for data-test
        }
    Missing translation keys fall back to the key itself so you can spot gaps.
    """
    resolved = []
    for alert in alerts_list or []:
        field_name = alert.get('field', '')

        # --- Section lookup: reverse map → section dict → country label ---
        section_dict = SECTION_BY_FIELD.get(field_name)
        section_labels = section_dict.get('labels', {}) if section_dict else {}
        section_label = section_labels.get(country_code, '') if section_dict else ''

        # --- Field label lookup: 'labels' dict indexed by country ---
        field_config = FIELDS.get(field_name, {})
        field_labels = field_config.get('labels', {})
        field_label = field_labels.get(country_code, field_name)

        # --- Type and reason: browser UI language ---
        type_key = alert.get('type_key', '')
        type_label = ui_strings.get(type_key, type_key)

        reason_key = alert.get('reason_key', '')
        reason_label = ui_strings.get(reason_key, reason_key)


        resolved.append({
            'severity':       _SEVERITY_TO_BOOTSTRAP.get(alert.get('severity', 'warning'), 'warning'),
            'type_label':      type_label,
            'reason_label':    reason_label,
            'raw_value':       alert.get('raw_value', alert.get('value', '')),
            'section_label':   section_label,
            'field_label':     field_label,
            'field_name':      field_name,
        })
    return resolved