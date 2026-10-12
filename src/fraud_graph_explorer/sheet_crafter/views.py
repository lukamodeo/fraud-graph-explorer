# src/fraud_graph_explorer/sheet_crafter/views.py

import os
import tempfile
from django.shortcuts import render
from django.http import FileResponse, Http404, HttpResponse
from django.utils.translation import get_language               # <== Used just to read browser setting
from .forms import SheetCrafterForm
from .services import generate_pdf_sheet, generate_dynamic_initial_data, get_calculated_tin
from .ui_translations import get_ui_strings


def calculate_tin_view(request):
    if request.method == 'POST':
        # HTMX flattens the JSON object into POST keys.
        fullname_key = request.POST.get('fullname')
        sex_key = request.POST.get('sex')         # <-- NEW
        dob_key = request.POST.get('dob')
        birthplace_key = request.POST.get('birthplace')
        tin_key = request.POST.get('tin')

        country = request.POST.get('country_code', 'IT')

        print(f"\n\n{tin_key} - {fullname_key} -{dob_key} - {birthplace_key}\n\n")

        if not all([fullname_key, sex_key, dob_key, birthplace_key, tin_key]):
            return HttpResponse("Error: Missing field mappings", status=400)

        # Fetch the actual values from the POST data using the dynamic keys
        form_data = {
            'fullname': request.POST.get(fullname_key, ''),
            'sex': request.POST.get(sex_key, ''),
            'dob': request.POST.get(dob_key, ''),
            'birthplace': request.POST.get(birthplace_key, ''),
        }

        # Calculate TIN using the service
        new_tin = get_calculated_tin(country, form_data)

        # Copy the POST data to a mutable dictionary and update the TIN value
        form_data_dict = request.POST.dict()
        form_data_dict[tin_key] = new_tin

        # Re-instantiate the form to let Django render the field perfectly
        form = SheetCrafterForm(form_data_dict, country_code=country, ui_strings=None)

        # Let Django render ONLY the specific field widget.
        # This guarantees 100% sync with forms.py (max_length, data-group, classes, etc.)
        return HttpResponse(form[tin_key].as_widget())

    return HttpResponse("Error", status=405)  # Method Not Allowed

def sheet_crafter_view(request):
    # Detect browser language for the UI
    browser_lang = get_language()

    # TODO no hard coded lang codes
    # Determine default country for the dropdown (and PDF labels)
    lang_code = browser_lang.lower()[:2]
    default_country = lang_code.upper() if lang_code.upper() in ['IT', 'DE', 'FR', 'ES'] else 'GB'

    # Handle all GET requests (both initial load and HTMX dropdown change)
    if request.method == 'GET':
        print("GET")
        # If HTMX changed the dropdown, use it. Otherwise use browser default.
        country = request.GET.get('country_code', default_country)

        # Now generate ui_strings, passing BOTH the browser lang AND the selected PDF country!
        ui_strings = get_ui_strings(browser_lang, country)

        # Generate initial data dynamically based on schema
        initial_data = generate_dynamic_initial_data(country)

        # Pass country_code to form for PDF labels, pass ui_strings to template
        form = SheetCrafterForm(initial=initial_data, country_code=country, ui_strings=ui_strings)

        # Reuse lang_code for the HTML lang attribute
        context = {
            'form': form,
            'ui': ui_strings,
            'active_lang': lang_code,
        }

        # If it's an HTMX request, return ONLY the form partial
        if request.headers.get('HX-Request'):
            return render(request, 'sheet_crafter/_form.html', context)

        # Otherwise, return the full page
        return render(request, 'sheet_crafter/sheet_crafter.html', context)

    # Handle POST requests (Generate PDF)
    if request.method == 'POST':
        print("POST")
        # Use default_country calculated at the top of the function as the fallback
        country = request.POST.get('country_code', default_country)
        print(f"POST_{country}")

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
            print(form.errors.as_json())
            print("-------------------------------")

    # Fallback for invalid POST
    # Use default_country for the UI strings here too
    print("POST Fallback")
    ui_strings = get_ui_strings(browser_lang, default_country)
    context = {
        # Fallback also uses dynamic generation
        'form': SheetCrafterForm(initial=generate_dynamic_initial_data(default_country), country_code=default_country, ui_strings=ui_strings),
        'ui': ui_strings,
        'active_lang': lang_code
    }
    return render(request, 'sheet_crafter/sheet_crafter.html', context)