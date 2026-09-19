# src/fraud_graph_explorer/sheet_crafter/forms.py
import json
from django import forms
from fraud_graph_explorer.graph_explorer.ingestion_schema import FIELDS, SECTIONS

class SheetCrafterForm(forms.Form):
    # COUNTRIES = [
    #     ('IT', 'Italy'),
    #     ('DE', 'Germany'),
    #     ('FR', 'France'),
    #     ('ES', 'Spain'),
    #     ('GB', 'United Kingdom'),   # <== default if not match
    # ]
    #
    # country_code = forms.ChoiceField(choices=COUNTRIES, label="Country")

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

        # def get_schema_label(internal_name):
        #     return FIELDS.get(internal_name, {}).get("labels", {}).get(cc, FIELDS[internal_name]["labels"]["GB"])

        # self.fields['request_number'].label = get_schema_label('request_number')
        # self.fields['company_name'].label = get_schema_label('company_name')
        # self.fields['company_vatn_taxc'].label = get_schema_label('company_vatn_taxc')
        # self.fields['legal_rep_name'].label = get_schema_label('legal_rep_name')
        # self.fields['legal_rep_dob'].label = get_schema_label('legal_rep_dob')
        # self.fields['taxcode_legal_representative'].label = get_schema_label('taxcode_legal_representative')

        # 1. Loop through sections to maintain the exact PDF layout order
        for section in SECTIONS:
            section_title = section["labels"].get(cc, section["labels"]["GB"])

            for internal_name in section["fields"]:
                field_config = FIELDS.get(internal_name)
                if not field_config:
                    continue

                # Read max_length from schema, default to 100
                max_length = field_config.get("max_length", 100)

                # 2. Create the form field dynamically
                # self.fields[internal_name] = forms.CharField(
                #     required=False,
                #     max_length=max_length
                # )

                # CHECK FOR HIDDEN ATTRIBUTE
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
                    # 3. Assign the localized label
                    labels = field_config.get("labels", {})
                    self.fields[internal_name].label = labels.get(cc, labels.get("GB", internal_name))

                # Attach the section title to the field so the template can use it
                self.fields[internal_name].section_title = section_title

                # Pass hint_key to template
                self.fields[internal_name].hint_key = field_config.get("hint_key", "")

                # Pass needs_tin_calc to template
                self.fields[internal_name].needs_tin_calc = field_config.get("needs_tin_calc", False)

                # Handle Sex Field Modal Trigger
                sex_field = field_config.get("sex_field")
                dob_field = field_config.get("dob_field")
                if sex_field and dob_field:
                    # Attach the names to the field object for the template
                    self.fields[internal_name].sex_field = sex_field
                    self.fields[internal_name].dob_field = dob_field

                    # ONLY inject the onchange trigger if the TIN is algorithmic!
                    if cc in ['IT', 'FR']:
                        self.fields[internal_name].widget.attrs.update({
                            'onchange': f"openTinDataDialog('{sex_field}', '{dob_field}')"
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
