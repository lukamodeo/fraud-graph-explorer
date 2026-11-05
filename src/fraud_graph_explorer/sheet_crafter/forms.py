# src/fraud_graph_explorer/sheet_crafter/forms.py

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

import json
from django import forms
from fraud_graph_explorer.domain_schema import FIELDS, SECTIONS

class SheetCrafterForm(forms.Form):

    country_code = forms.ChoiceField(label="Country")

    def __init__(self, *args, country_code="GB", ui_strings=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Grab the list of tuples directly from the UI dictionary
        ui = ui_strings or {}
        self.fields['country_code'].choices = ui.get("COUNTRY_FLAGS_NAMES", [])

        self.fields['country_code'].widget.attrs.update({
            'hx-get': '.',
            'hx-target': '#form-container',
            'hx-trigger': 'change',
            'autocomplete': 'nope',
            'hx-push-url': 'true',
        })

        cc = country_code.upper()

        # Loop through sections to maintain the exact PDF layout order
        for section in SECTIONS:
            section_title = section["labels"].get(cc, section["labels"]["GB"])

            for internal_name in section["fields"]:
                field_config = FIELDS.get(internal_name)
                if not field_config:
                    continue

                # Read max_length from schema, default to 100
                max_length = field_config.get("max_length", 100)

                # Check for hidden attribute
                if field_config.get("hidden"):
                    self.fields[internal_name] = forms.CharField(
                        required=False,
                        max_length=max_length,
                        widget=forms.HiddenInput()
                    )
                else:
                    self.fields[internal_name] = forms.CharField(
                        required=False,
                        max_length=max_length
                    )
                    # Assign the localized label
                    labels = field_config.get("labels", {})
                    self.fields[internal_name].label = labels.get(cc, labels.get("GB", internal_name))

                # Attach the section title to the field so the template can use it
                self.fields[internal_name].section_title = section_title

                # Pass hint_key to template
                self.fields[internal_name].hint_key = field_config.get("hint_key", "")

                # Pass needs_tin_calc to template
                self.fields[internal_name].needs_tin_calc = field_config.get("needs_tin_calc", False)

                # Handle Fields Modal Trigger
                sex_field = field_config.get("sex_field")
                dob_field = field_config.get("dob_field")
                tin_field = field_config.get("tin_field")
                if sex_field and dob_field and tin_field:
                    # Attach the names to the field object for the template
                    self.fields[internal_name].sex_field = sex_field
                    self.fields[internal_name].dob_field = dob_field

                    # Always attach — the JS checks the TIN's override country select
                    # to decide whether to actually fire the modal
                    self.fields[internal_name].widget.attrs.update({
                        'onchange': f"openTinDataDialog('{sex_field}', '{dob_field}', '{tin_field}')"
                        })
                else:
                    self.fields[internal_name].sex_field = ""
                    self.fields[internal_name].dob_field = ""

                # Convert dict to json string
                calc_fields = field_config.get("calc_fields")
                #print(f"DEBUG: {internal_name} — schema has calc_fields: {calc_fields is not None}, value: {calc_fields}")
                if calc_fields:
                    self.fields[internal_name].calc_fields = json.dumps(calc_fields)
                    # include_ids = []
                    # for key, fname in calc_fields.items():
                    #     if key != 'tin':   # don't include the TIN field itself
                    #         include_ids.append(f"#id_{fname}")
                    include_ids = [f"#id_{fname}" for fname in calc_fields.values()]
                    self.fields[internal_name].hx_include_fields = ",".join(include_ids)
                else:
                    self.fields[internal_name].calc_fields = ""
                    self.fields[internal_name].hx_include_fields = ""

                # ─── NEW: Attach tags + fake_type for template logic (country override selects) ───
                self.fields[internal_name].tags = field_config.get("tags", [])
                self.fields[internal_name].fake_type = field_config.get("fake_type", "")

                # Determine if this field supports country override (VAT, TIN, or IBAN)
                is_override_field = any(t in field_config.get("tags", []) for t in ("VAT", "TIN", "IBAN"))
                self.fields[internal_name].is_country_override = is_override_field
                # ──────────────────────────────────────────────────────────────────────────────────