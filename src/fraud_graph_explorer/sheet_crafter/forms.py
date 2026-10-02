# src/fraud_graph_explorer/sheet_crafter/forms.py
import json
from django import forms
from fraud_graph_explorer.domain_schema import FIELDS, SECTIONS

class SheetCrafterForm(forms.Form):

    country_code = forms.ChoiceField(label="Country")

    def __init__(self, *args, country_code="GB", ui_strings=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Grab the list of tuples directly from the UI dictionary
        ui = ui_strings or {}
        self.fields['country_code'].choices = ui.get("COUNTRY_NAMES", [])

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
                self.fields[internal_name].needs_tin_calc = field_config.get("needs_tin_calc", False) if cc in ['IT', 'FR'] else False

                # Handle Fields Modal Trigger
                sex_field = field_config.get("sex_field")
                dob_field = field_config.get("dob_field")
                tin_field = field_config.get("tin_field")
                if sex_field and dob_field and tin_field:
                    # Attach the names to the field object for the template
                    self.fields[internal_name].sex_field = sex_field
                    self.fields[internal_name].dob_field = dob_field

                    # ONLY inject the onchange trigger if the TIN is algorithmic!
                    if cc in ['IT', 'FR']:
                        self.fields[internal_name].widget.attrs.update({
                            'onchange': f"openTinDataDialog('{sex_field}', '{dob_field}', '{tin_field}')"
                        })
                else:
                    self.fields[internal_name].sex_field = ""
                    self.fields[internal_name].dob_field = ""

                # Convert dict to json string
                calc_fields = field_config.get("calc_fields")
                if calc_fields:
                    self.fields[internal_name].calc_fields = json.dumps(calc_fields)
                else:
                    self.fields[internal_name].calc_fields = ""
