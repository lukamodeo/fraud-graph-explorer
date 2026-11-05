# src/fraud_graph_explorer/sheet_crafter/views.py

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

import os
import json
import tempfile

from django.shortcuts import render
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required

from .forms import SheetCrafterForm
from .services import generate_pdf_sheet, generate_dynamic_initial_data, get_calculated_tin
from .ui_translations import get_ui_strings
from .seed_data import get_random_data, get_random_profile
from fraud_graph_explorer.domain_schema import FIELDS, CountryCodes
from fraud_graph_explorer.validators.country_detection import detect_tin_country

# HELPER FUNCTIONS
def _extract_hints(ui_strings, country):
    """
    Extract country-specific hints from ui_strings.
    Returns (resolved_hints, hints_json) for template + JS.

    - resolved_hints: dict with the INITIAL tooltip text (for the sheet's country)
    - hints_json: JSON string of ALL per-country hints (for JS to use on select change)
    """
    hints_by_country = {
        'HINT_VAT': ui_strings.get('HINT_VAT', {}),
        'HINT_TIN': ui_strings.get('HINT_TIN', {}),
        'HINT_IBAN': ui_strings.get('HINT_IBAN', {}),
    }
    resolved_hints = {}
    for hint_key, hint_val in hints_by_country.items():
        if isinstance(hint_val, dict):
            # "ANY"-wrapped — look up the sheet's country
            resolved_hints[hint_key] = hint_val.get(country, hint_val.get('GB', ''))
        else:
            # 1D — use as-is
            resolved_hints[hint_key] = hint_val
    return resolved_hints, json.dumps(hints_by_country)


@login_required
def generate_field_value(request):
    """
    HTMX endpoint: regenerate a single field's value when its country
    override dropdown changes.

    GET params:
        field:        internal field name (e.g., 'company_vat')
        country:      override country code (from the select's value)
        sheet_country: the sheet's country (for context)
        + any form field values included via hx-include (for TIN calc)

    Returns: the new value as plain text (HTMX swaps it into the input).
    """


    field_name = request.GET.get('field', '')
    sheet_country = request.GET.get('sheet_country', 'GB').upper()

    # ─── FIX: The select's name is "{field_name}_country" (dynamic per-field),
    # so we can't look for a fixed "country" key. Scan for any *_country param. ───
    override_country = ''
    for key in request.GET:
        if key.endswith('_country'):
            override_country = request.GET[key].upper()
            break


    if not field_name or not override_country:
        return JsonResponse({'value': '', 'updates': {}})

    config = FIELDS.get(field_name, {})
    tags = config.get('tags', [])
    updates = {}

    if 'VAT' in tags:
        value = get_random_data(override_country, 'vat')

    elif 'IBAN' in tags:
        value = get_random_data(override_country, 'iban')

    elif 'TIN' in tags:
        if override_country in ('IT', 'FR'):
            # Algorithmic TIN — need fullname/sex/dob/birthplace from the form
            calc_fields = config.get('calc_fields', {})

            # Build the calc data dict from the form's hidden fields
            calc_data = {
                'fullname':    request.GET.get(calc_fields.get('fullname', ''), ''),
                'sex':         request.GET.get(calc_fields.get('sex', ''), ''),
                'dob':         request.GET.get(calc_fields.get('dob', ''), ''),
                'birthplace':  request.GET.get(calc_fields.get('birthplace', ''), ''),
            }

            # Snapshot original values to detect what get_calculated_tin() resolved
            original_dob = calc_data['dob']
            original_birthplace = calc_data['birthplace']

            value = get_calculated_tin(override_country, calc_data)

            # calc_data is now mutated with resolved dob/birthplace.
            # Send updates only for fields that actually changed.
            if calc_data['dob'] != original_dob:
                updates[calc_fields.get('dob', '')] = calc_data['dob']
            if calc_data['birthplace'] != original_birthplace:
                updates[calc_fields.get('birthplace', '')] = calc_data['birthplace']
        else:
            # DE/ES/GB: pick from the override country's TIN pool
            profile = get_random_profile(override_country)
            value = profile['tin']

    else:
        value = ''

    # Uniform contract: always JSON, always {value, updates}
    return JsonResponse({'value': value, 'updates': updates})

@login_required
def calculate_tin_view(request):

    print(f"==> CALCULATE_TIN_VIEW")

    if request.method == 'POST':
        # HTMX flattens the JSON object into POST keys.
        fullname_key = request.POST.get('fullname')
        sex_key = request.POST.get('sex')
        dob_key = request.POST.get('dob')
        birthplace_key = request.POST.get('birthplace')
        tin_key = request.POST.get('tin')


        if not all([fullname_key, sex_key, dob_key, birthplace_key, tin_key]):
            return HttpResponse("Error: Missing field mappings", status=400)

        # ─── Read override country ───
        # The TIN's country select has name="{tin_key}_country" (e.g., "representative_tin_country")
        # Look for it SPECIFICALLY first, then fall back to scanning
        tin_country_key = f"{tin_key}_country"
        override_country = request.POST.get(tin_country_key, '').upper()

        print(f"tin_country_key: {tin_country_key!r}")
        print(f"override_country from specific key: {override_country!r}")

        if not override_country:
            # Fall back: scan for any *_country param
            for key in request.POST:
                if key.endswith('_country'):
                    override_country = request.POST[key].upper()
                    print(f"Found via scan: {key}={override_country!r}")
                    break

        # Fall back to the sheet's country if no override select was found
        country_code = override_country or request.POST.get('country_code', 'GB')
        print(f"final country_code: {country_code!r}")


        if not all([fullname_key, sex_key, dob_key, birthplace_key, tin_key]):
            return HttpResponse("Error: Missing field mappings", status=400)


        # Fetch the actual values from the POST data using the dynamic keys
        form_data = {
            'fullname': request.POST.get(fullname_key, ''),
            'sex': request.POST.get(sex_key, ''),
            'dob': request.POST.get(dob_key, ''),
            'birthplace': request.POST.get(birthplace_key, ''),
        }

        # ─── Calculate TIN based on country ───
        if country_code in ('IT', 'FR'):
            new_tin = get_calculated_tin(country_code, form_data)
        else:
            # DE/ES/GB: TIN is not algorithmic.
            # If the current TIN is already valid for this country, keep it —
            # the user clicked recalc but the value is fine, no reason to change it.
            # Only pull from the pool if the current value is invalid/empty
            # or belongs to a different country.
            current_tin = request.POST.get(tin_key, '').strip()
            if current_tin and detect_tin_country(current_tin) == country_code:
                new_tin = current_tin
            else:
                profile = get_random_profile(country_code)
                new_tin = profile['tin']

        print(f"==> CALCULATE_TIN_VIEW - NEW TIN: {new_tin}")

        # Copy the POST data to a mutable dictionary and update the TIN value
        form_data_dict = request.POST.dict()
        form_data_dict[tin_key] = new_tin

        # Re-instantiate the form to let Django render the field perfectly
        form = SheetCrafterForm(form_data_dict, country_code=country_code, ui_strings=None)

        # Let Django render ONLY the specific field widget.
        # This guarantees 100% sync with forms.py (max_length, data-group, classes, etc.)
        return HttpResponse(form[tin_key].as_widget())

    return HttpResponse("Error", status=405)  # Method Not Allowed

@login_required
def sheet_crafter_view(request):
    # Detect browser language for the UI
    browser_lang = get_language()

    # Determine default country for the dropdown (and PDF labels)
    lang_code = browser_lang.lower()[:2]

    # Derive valid country codes from the enum (no hardcoding)
    target_country_codes = {code.value for code in CountryCodes}
    default_country = lang_code.upper() if lang_code.upper() in target_country_codes else 'GB'

    # Handle all GET requests (both initial load and HTMX dropdown change)
    if request.method == 'GET':
        # If HTMX changed the dropdown, use it. Otherwise use browser default.
        country = request.GET.get('country_code', default_country)

        # Now generate ui_strings, passing BOTH the browser lang AND the selected PDF country!
        ui_strings = get_ui_strings(browser_lang, country)

        # Generate initial data dynamically based on schema
        initial_data = generate_dynamic_initial_data(country)

        # Pass country_code to form for PDF labels, pass ui_strings to template
        form = SheetCrafterForm(initial=initial_data, country_code=country, ui_strings=ui_strings)

        resolved_hints, hints_json = _extract_hints(ui_strings, country)   # ← NEW
        modal_recalc_labels_json = json.dumps(ui_strings.get('MODAL_RECALC_TIN_LABEL', {}))

        # Reuse lang_code for the HTML lang attribute
        context = {
            'form': form,
            'ui': ui_strings,
            'active_lang': lang_code,
            'resolved_hints': resolved_hints,
            'hints_json': hints_json,
            'modal_recalc_labels_json': modal_recalc_labels_json
        }

        # If it's an HTMX request, return ONLY the form partial
        if request.headers.get('HX-Request'):
            return render(request, 'sheet_crafter/_form.html', context)

        # Otherwise, return the full page
        return render(request, 'sheet_crafter/sheet_crafter.html', context)

    # Handle POST requests (Generate PDF)
    if request.method == 'POST':
        # Use default_country calculated at the top of the function as the fallback
        country = request.POST.get('country_code', default_country)

        # Generate ui_strings for POST too, in case the form fails validation and re-renders
        ui_strings = get_ui_strings(browser_lang, country)
        form = SheetCrafterForm(request.POST, country_code=country, ui_strings=ui_strings)

        if form.is_valid():
            # Extract the request number from the form
            request_number = form.cleaned_data.get('request_number', 'UNKNOWN')

            # Sanitize it to ensure it's a valid filename
            # (Removes spaces or special characters, allows dashes/underscores)
            safe_filename = "".join(c for c in request_number if c.isalnum() or c in ('-', '_')).rstrip()
            filename = f"{safe_filename}.pdf"

            # Create a temporary file path in the OS temp folder
            temp_dir = tempfile.gettempdir()
            filepath = os.path.join(temp_dir, filename)

            # Generate it
            generate_pdf_sheet(country, form.cleaned_data, filepath)

            # Serve the file to the user for download
            if os.path.exists(filepath):
                response = FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)
                return response
            raise Http404("PDF generation failed.")
        else:
            print("--- FORM VALIDATION FAILED ---")
            print(f"Errors: {form.errors.as_json()}")
            print(f"POST country_code: {request.POST.get('country_code')!r}")
            print(f"POST keys: {list(request.POST.keys())}")
            print("-------------------------------")

            # ─── FIX: Re-render WITH the user's submitted data (don't lose edits) ───
            resolved_hints, hints_json = _extract_hints(ui_strings, country)
            modal_recalc_labels_json = json.dumps(ui_strings.get('MODAL_RECALC_TIN_LABEL', {}))
            context = {
                'form': form,                       # ← reuse the invalid form (preserves user's data)
                'ui': ui_strings,
                'active_lang': lang_code,
                'resolved_hints': resolved_hints,
                'hints_json': hints_json,
                'modal_recalc_labels_json': modal_recalc_labels_json
            }
            return render(request, 'sheet_crafter/sheet_crafter.html', context)