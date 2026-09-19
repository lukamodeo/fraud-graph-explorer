# src/fraud_graph_explorer/sheet_crafter/views.py

import os
import uuid
from django.shortcuts import render
from django.http import FileResponse, Http404, HttpResponse
from django.utils.translation import get_language               # <== Used just to read browser setting
from .forms import SheetCrafterForm
from .services import generate_pdf_sheet, generate_dynamic_initial_data
#from .seed_data import get_random_profile
from .ui_translations import get_ui_strings



def calculate_tax_code_view(request):
    if request.method == 'POST':
        print(request.POST)

        # HTMX flattens the JSON object into POST keys.
        tin_key = request.POST.get('tin')
        name_key = request.POST.get('name')
        dob_key = request.POST.get('dob')
        birthplace_key = request.POST.get('birthplace')

        print(f"\n\n{tin_key} - {name_key} -{dob_key} - {birthplace_key}\n\n")

        if not all([tin_key, name_key, dob_key, birthplace_key]):
            return HttpResponse("Error: Missing field mappings", status=400)

        # Fetch the actual values from the POST data using the dynamic keys
        name = request.POST.get(name_key, '')
        dob = request.POST.get(dob_key, '')
        birthplace = request.POST.get(birthplace_key, '')
        country = request.POST.get('country_code', 'IT')

        # Placeholder logic for Italian Codice Fiscale
        if country == 'IT' and name and dob and birthplace:
            # MOCK CALCULATION (Replace with your actual CF library later)
            reversed_name = name.upper().replace(" ", "")[:6]
            year = dob[2:4]
            month = dob[5:7]
            day = dob[8:10]
            new_tin = f"{reversed_name}{year}{month}{day}{birthplace}X"
        else:
            new_tin = "CALCULATION_FAILED"

        # return HttpResponse(f'<input type="text" name="representative_taxcode" id="id_representative_taxcode" value="{new_tin}" maxlength="20">')

        # Copy the POST data to a mutable dictionary and update the TIN value
        form_data = request.POST.dict()
        form_data[tin_key] = new_tin

        # Re-instantiate the form with the updated data
        form = SheetCrafterForm(form_data, country_code=country)

        # Let Django render ONLY the specific field widget.
        # This guarantees 100% sync with forms.py (max_length, data-group, classes, etc.)
        return HttpResponse(form[tin_key].as_widget())

    return HttpResponse("Error", status=405)  # Method Not Allowed

def sheet_crafter_view(request):
    # Detect browser language for the UI
    browser_lang = get_language()
    #ui_strings = get_ui_strings(browser_lang)

    # Determine default country for the dropdown (and PDF labels)
    lang_prefix = browser_lang.lower()[:2]
    default_country = lang_prefix.upper() if lang_prefix.upper() in ['IT', 'DE', 'FR', 'ES'] else 'GB'

    # Handle all GET requests (both initial load and HTMX dropdown change)
    if request.method == 'GET':
        # If HTMX changed the dropdown, use it. Otherwise use browser default.
        country = request.GET.get('country_code', default_country)

        # NOW generate ui_strings, passing BOTH the browser lang AND the selected PDF country!
        ui_strings = get_ui_strings(browser_lang, country)

        # Generate initial data dynamically based on schema
        initial_data = generate_dynamic_initial_data(country)

        # Pass country_code to form for PDF labels, pass ui_strings to template
        form = SheetCrafterForm(initial=initial_data, country_code=country, ui_strings=ui_strings)

        # Reuse lang_prefix for the HTML lang attribute
        context = {
            'form': form,
            'ui': ui_strings,
            'active_lang': lang_prefix,
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

            # Sanitize it slightly to ensure it's a valid filename
            # (Removes spaces or special characters, allows dashes/underscores)
            safe_filename = "".join(c for c in request_number if c.isalnum() or c in ('-', '_')).rstrip()

            # Use it for the filename
            filename = f"{safe_filename}.pdf"
            filepath = os.path.join('media', 'pdfs', country, filename)

            # Generate it
            generate_pdf_sheet(country, form.cleaned_data, filepath)

            # Serve the file to the user for download
            if os.path.exists(filepath):
                return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)
            raise Http404("PDF generation failed.")

    # Fallback for invalid POST
    # Use default_country for the UI strings here too
    ui_strings = get_ui_strings(browser_lang, default_country)
    context = {
        # Fallback also uses dynamic generation
        'form': SheetCrafterForm(initial=generate_dynamic_initial_data(default_country), country_code=default_country, ui_strings=ui_strings),
        'ui': ui_strings,
        'active_lang': lang_prefix
    }
    return render(request, 'sheet_crafter/sheet_crafter.html', context)