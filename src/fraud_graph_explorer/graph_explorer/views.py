# src/fraud_graph_explorer/graph_explorer/views.py

import os
import re
import json
import base64
import tempfile

from urllib.parse import urlparse, parse_qs, urlencode

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Count, Exists, OuterRef, Subquery
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.utils.translation import get_language
from django.views.decorators.http import require_POST

from .alerts import resolve_alerts
from .models import Application, Entity, UsesIdentifier
from .services import ingest_pdf, annotate_has_links
from .ui_translations import get_ui_strings
from fraud_graph_explorer.domain_schema import FIELDS, SECTIONS, ENTITY_GRAPH_META, CountryCodes, get_country_flag


# HELPER FUNCTIONS
def _format_sheet_label(app, ui_strings):
    """
    Builds a multi-line HTML label for a Vis.js Sheet node.
    Includes the Country Flag on top, Request Info, and Company Info with Short Localized Labels.
    """
    flag = get_country_flag(app.country_code)

    # Fetch short labels from UI dictionary
    req_label = ui_strings.get("GRAPH_LBL_REQ", "Loan Application")
    branch_label = ui_strings.get("GRAPH_LBL_BRANCH", "Branch")
    #comp_name_label = ui_strings.get("GRAPH_LBL_COMPANY", "Company")
    comp_loc_label = ui_strings.get("GRAPH_LBL_LOC", "Registered Office")
    comp_vat_label = ui_strings.get("GRAPH_LBL_VAT", "VAT R.No.")

    # Safely get values, fallback to empty string if missing
    req_num = app.request_number or "N/A"
    branch = app.request_branch_location or "N/A"
    comp_name = app.company_name or "N/A"
    comp_loc = app.company_location or "N/A"
    comp_vat = app.company_vat or "N/A"

    # Build the string cleanly without indentation issues
    label = (
        f"<b><i>{flag}</i></b>\n"
        f"<i>{req_label}</i>\n\n"
        f"<b>{req_num}</b> - <i>{branch_label}:</i> {branch}\n\n"
        f"<code>{comp_name}</code>\n"
        f"(<i>{comp_loc_label}</i>:  {comp_loc})\n\n"
        f"<i>{comp_vat_label}</i>\n"
        f"<code>{comp_vat}</code>\n"
    )
    return label


def _get_translated_field_context(internal_name, country_code):
    """
    Resolves an internal_name (e.g., 'representative_fullname')
    into a translated string: "Section Title: Field Label"
    based on the document's country code.
    """
    if not internal_name:
        return "Unknown Field"

    cc = country_code.upper() if country_code else 'GB'

    # Find the field label
    field_config = FIELDS.get(internal_name, {})
    field_labels = field_config.get("labels", {})
    field_label = field_labels.get(cc, field_labels.get("GB", internal_name))

    # Find the parent section label
    section_label = ""
    for section in SECTIONS:
        if internal_name in section.get("fields", []):
            sec_labels = section.get("labels", {})
            section_label = sec_labels.get(cc, sec_labels.get("GB", ""))
            break

    if section_label:
        return f"{section_label}: {field_label}"
    return field_label


def _entity_icon_view(request, entity_type):
    """
    Generates a dynamic SVG image with a white background and the Bootstrap Icon.
    Vis.js fetches this to render clean entity nodes without transparent edges.
    """
    meta = ENTITY_GRAPH_META.get(entity_type)
    if not meta:
        return HttpResponse(status=404)

    # Read the local Bootstrap Icons font file
    font_path = os.path.join(settings.BASE_DIR, 'static', 'vendor', 'css', 'fonts', 'bootstrap-icons.woff2')
    try:
        with open(font_path, 'rb') as f:
            font_base64 = base64.b64encode(f.read()).decode('utf-8')
    except FileNotFoundError:
        return HttpResponse(status=500)

    icon_code = meta['bs_icon']
    icon_color = meta['color']

    # Build the SVG string
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 50 50">
        <style>
            @font-face {{
                font-family: 'bootstrap-icons';
                src: url(data:font/woff2;base64,{font_base64}) format('woff2');
            }}
        </style>
        <circle cx="25" cy="25" r="24" fill="#ffffff" stroke="#dddddd" stroke-width="1"/>
        <text x="25" y="38" font-family="bootstrap-icons" font-size="26" fill="{icon_color}" text-anchor="middle">{icon_code}</text>
    </svg>'''

    return HttpResponse(svg, content_type="image/svg+xml")


@require_POST
def delete_application_view(request, sheet_id):
    """
    Deletes an Application, cleans up orphans, and returns the correct
    filtered URL to redirect the list to Page 1.
    """
    app = get_object_or_404(Application, sheet_id=sheet_id)

    if app.pdf_file:
        app.pdf_file.delete(save=False)

    app.delete()
    Entity.objects.annotate(num_apps=Count('applications')).filter(num_apps=0).delete()

    # Get filters from the Referer URL (the page the user is currently on)
    referer = request.headers.get('Referer', '')
    parsed_url = urlparse(referer)
    params = parse_qs(parsed_url.query)

    # Extract individual filters
    query = params.get('q', [''])[0]
    country = params.get('country', [''])[0]
    status = params.get('status', [''])[0]
    start_date = params.get('start_date', [''])[0]
    end_date = params.get('end_date', [''])[0]

    # Check if the filtered list is now EMPTY
    qs = Application.objects.all()
    if query:
        q_objs = Q(request_number__icontains=query) | Q(company_name__icontains=query) | Q(company_vat__icontains=query) | Q(entities__value__icontains=query)
        qs = qs.filter(q_objs).distinct()
    if country: qs = qs.filter(country_code=country)
    if status:
        if status == 'ok':
            qs = qs.filter(has_validation_errors=False, has_rule_warnings=False)
        elif status == 'err':
            qs = qs.filter(has_validation_errors=True)
        elif status == 'warn':
            qs = qs.filter(has_rule_warnings=True)
        elif status == 'err_or_warn':
            qs = qs.filter(Q(has_validation_errors=True) | Q(has_rule_warnings=True))
    if start_date: qs = qs.filter(acquisition_date__date__gte=start_date)
    if end_date: qs = qs.filter(acquisition_date__date__lte=end_date)

    # Build the target URL for JavaScript
    if not qs.exists():
        # List is empty! Clear all filters.
        target_url = "/explorer/"
    else:
        # Keep filters, but omit 'page' so it defaults to Page 1
        query_dict = {}
        if query: query_dict['q'] = query
        if country: query_dict['country'] = country
        if status: query_dict['status'] = status
        if start_date: query_dict['start_date'] = start_date
        if end_date: query_dict['end_date'] = end_date

        query_string = urlencode(query_dict)
        target_url = f"/explorer/?{query_string}" if query_string else "/explorer/"

    # Return the target URL in a custom event payload
    response = HttpResponse('')
    response['HX-Trigger'] = json.dumps({
        'deleteSuccess': {
            'value':    target_url,         # existing
            'sheet_id': str(sheet_id),      # string, since UUIDs aren't JSON-native
        }
    })
    return response


def dashboard_view(request):
    # Base Queryset - Filtering & Pagination Logic
    queryset = Application.objects.all().order_by('-acquisition_date')

    # Search logic (wildcards)
    query = request.GET.get('q', '').strip()
    country = request.GET.get('country', '')
    status = request.GET.get('status', '')
    start_date = request.GET.get('start_date', '').strip()
    end_date = request.GET.get('end_date', '').strip()

    active_filters = []

    if query:
        # Safely handle wildcards using Regex
        # Escape all regex special chars (like ., +, ?) EXCEPT our *
        safe_query = re.escape(query).replace(r'\*', '.*')
        q_objects = Q(request_number__iregex=safe_query)
        q_objects |= Q(company_name__iregex=safe_query)
        q_objects |= Q(company_vat__iregex=safe_query)
        q_objects |= Q(entities__value__iregex=safe_query)
        queryset = queryset.filter(q_objects).distinct()
        active_filters.append({"key": "q", "value": query})

    if country:
        queryset = queryset.filter(country_code=country)
        active_filters.append({"key": "country", "value": country})

    if status:
        if status == 'ok':
            queryset = queryset.filter(has_validation_errors=False, has_rule_warnings=False)
        elif status == 'err':
            queryset = queryset.filter(has_validation_errors=True)
        elif status == 'warn':
            queryset = queryset.filter(has_rule_warnings=True)
        elif status == 'err_or_warn':
            queryset = queryset.filter(Q(has_validation_errors=True) | Q(has_rule_warnings=True))
        active_filters.append({
                                  "key": "status",
                                  "value": status
                                  })

    if start_date:
        queryset = queryset.filter(acquisition_date__date__gte=start_date)
        active_filters.append({"key": "start_date", "value": start_date})
    if end_date:
        queryset = queryset.filter(acquisition_date__date__lte=end_date)
        active_filters.append({"key": "end_date", "value": end_date})

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    page_items = annotate_has_links(page_obj.object_list)

    # Get UI strings from graph_explorer
    browser_lang = get_language()
    ui_strings = get_ui_strings(browser_lang)

    # Build a map for country badges: {"IT": "Italia", "DE": "Germania", ...}
    country_names_map = dict(ui_strings.get("COUNTRY_NAMES", []))

    # Format the pagination string with current page and total pages
    pag_template = ui_strings.get("PAG_PAGE_OF", "Page {current} of {total}")
    ui_strings["PAG_PAGE_OF"] = pag_template.format(
        current=page_obj.number,
        total=page_obj.paginator.num_pages
    )

    # Build dynamic list columns from schema
    list_columns = []
    for internal_name, config in FIELDS.items():
        if config.get("list_view"):
            list_label_key = config.get("list_label", internal_name)
            label = ui_strings.get(list_label_key, internal_name)
            list_columns.append({"key": internal_name, "label": label})

    # Build a dynamic dictionary of flags: {'IT': '🇮🇹', 'DE': '🇩🇪', ...}
    country_flags = {code.value: get_country_flag(code.value) for code in CountryCodes}


    context = {
        'page_obj': page_obj,
        'page_items': page_items,
        'query': query,
        'country_filter': country,
        'status_filter': status,
        'start_date': start_date,
        'end_date': end_date,
        'country_flags': country_flags,
        'country_names_map': country_names_map,
        'list_columns': list_columns,
        'ui': ui_strings,
        'active_filters': active_filters
        }

    # If HTMX request, return ONLY the table partial
    if request.headers.get('HX-Request'):
        return render(request, 'graph_explorer/_sheet_list.html', context)

    # If normal browser load (F5), return the full dashboard
    legend_items = []
    js_groups = {}

    # Build dynamic data for HTML Legend and JS Vis.js groups
    for entity_type, meta in ENTITY_GRAPH_META.items():
        label = ui_strings.get(meta['label_key'], entity_type)
        legend_items.append({
            'type': entity_type,
            'css_icon': meta['css_icon'],
            'color': meta['color'],
            'label': label
            })

        # Build the Vis.js group configuration dynamically
        js_groups[entity_type] = {
            'shape': 'circularImage',
            'image': f'/explorer/api/icon/{entity_type}/',
            'size': 20,
            'font': {
                'color': '#2c3e50',
                'background': '#ffffff'
                }
            }

    context['legend_items'] = legend_items
    context['js_groups'] = json.dumps(js_groups)

    return render(request, 'graph_explorer/dashboard.html', context)


def ingest_pdf_view(request):
    # Get UI strings for translation
    browser_lang = get_language()
    ui = get_ui_strings(browser_lang)

    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        country = request.POST.get('country_code', 'GB') # Fallback

        # Read bytes from uploaded file
        pdf_bytes = pdf_file.read()

        # Run ingestion service!
        app, error_code, existing_app = ingest_pdf(pdf_bytes, country, pdf_file.name, overwrite=False)

        # Handle Success
        if app:
            msg = ui.get("INGEST_SUCCESS", "Ingested: {req_num}").format(req_num=app.request_number)
            response = HttpResponse(f'<span class="badge text-bg-success">{msg}</span>')
            response['HX-Trigger'] = json.dumps({
                #"refreshList": True,
                "selectNewApp": str(app.sheet_id)
            })
            return response

        elif error_code == "duplicate" and existing_app:
            # Save the uploaded bytes to the OS Temp Folder
            # delete=False is crucial, otherwise Python deletes it as soon as the function ends!
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(pdf_bytes)
                temp_file_name = os.path.basename(temp_file.name)

            # Render the modal asking for confirmation
            msg = ui.get("DUP_MSG", "Duplicate: {req_num}").format(
                req_num=existing_app.request_number,
                old_file=existing_app.file_name
            )

            context={
                'ui': ui,
                'temp_file_name': temp_file_name,
                'country_code': country,
                'file_name': pdf_file.name,
                'dup_msg': msg
            }

            # Render the modal HTML
            modal_html = render_to_string(
                request=request,    # ADD request so the csrf token is available in the template
                template_name='graph_explorer/_duplicate_modal.html',
                context=context
            )

            # Return OOB swaps: Clear status badge area, inject modal into #modal-container
            response_html = f'''
            <div hx-swap-oob="true" id="ingest-status"></div>
            <div hx-swap-oob="true" id="modal-container">{modal_html}</div>
            '''
            return HttpResponse(response_html)

        elif error_code == "invalid_sheet":
            msg = ui.get("INGEST_ERR_INVALID_SHEET", "Failed")
            return HttpResponse(f'<span class="badge text-bg-danger">{msg}</span>')

        elif error_code == "parse_error":
            msg = ui.get("INGEST_ERR_PARSE_ERROR", "Failed")
            return HttpResponse(f'<span class="badge text-bg-danger">{msg}</span>')

        else:
            msg = ui.get("INGEST_ERR_UNKNOWN", "Failed")
            return HttpResponse(f'<span class="badge text-bg-danger">{msg}</span>')

    msg = ui.get("INGEST_ERR_NO_FILE", "No file uploaded.")
    return HttpResponse(f'<span class="badge text-bg-danger">{msg}</span>')


def ingest_confirm_view(request):
    browser_lang = get_language()
    ui = get_ui_strings(browser_lang)

    if request.method == 'POST':
        temp_file_name = request.POST.get('temp_file_name')
        country = request.POST.get('country_code', 'IT')
        file_name = request.POST.get('file_name')

        # Reconstruct the full path to the OS temp file
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, temp_file_name)

        try:
            # Read the bytes back
            with open(temp_path, 'rb') as f:
                pdf_bytes = f.read()
        except FileNotFoundError:
            return HttpResponse('<span class="badge badge-err">Error: Temp file lost.</span>')

        # Delete the temp file immediately
        os.unlink(temp_path)

        # Call ingest_pdf with overwrite=True!
        app, error_code, _ = ingest_pdf(pdf_bytes, country, file_name, overwrite=True)

        if app:
            msg = ui.get("INGEST_OVERWRITTEN", "Overwritten: {req_num}").format(req_num=app.request_number)
            # Tell the browser to trigger the events on overwrite success
            response = HttpResponse(f'<span class="badge text-bg-success">{msg}</span>')
            response['HX-Trigger'] = json.dumps({
                #"refreshList": True,
                "selectNewApp": str(app.sheet_id)
            })
            return response
        else:
            msg = ui.get("INGEST_ERR_UNKNOWN")
            return HttpResponse(f'<span class="badge text-bg-danger">{msg}</span>')

    return HttpResponse("Method not allowed", status=405)


def sheet_detail_view(request, sheet_id):
    app = get_object_or_404(Application, sheet_id=sheet_id)

    # Get 2D UI Strings for THIS specific application's country
    browser_lang = get_language()
    ui_strings = get_ui_strings(browser_lang, app.country_code)

    # Resolve JSON error/warning keys into final translated strings
    resolved_errors = []
    for err in app.validation_errors:
        reason = ui_strings.get(err.get("reason_key", ""), err.get("reason_key", ""))
        resolved_errors.append({"type": ui_strings.get(err.get("type_key", ""), ""), "reason": reason})

    resolved_warnings = []
    for warn in app.rule_warnings:
        reason = ui_strings.get(warn.get("reason_key", ""), warn.get("reason_key", ""))
        resolved_warnings.append({"type": ui_strings.get(warn.get("type_key", ""), ""), "reason": reason})

    # Reconstruct the PDF layout from DB for the detail pane
    detail_sections = []
    edges = app.usesidentifier_set.all()
    edge_dict = {edge.source_field: edge.entity.value for edge in edges}

    cc = app.country_code
    for section in SECTIONS:
        sec_data = {
            "title": section["labels"].get(cc, section["labels"]["GB"]),
            "rows": []
        }
        for internal_name in section.get("fields", []):
            config = FIELDS.get(internal_name, {})
            if config.get("hidden"): continue

            label = config.get("labels", {}).get(cc, internal_name)
            # Get value from Sheet column or Edge
            value = getattr(app, internal_name, None) or edge_dict.get(internal_name, "")
            sec_data["rows"].append({
                "label": label,
                "value": value
            })
        detail_sections.append(sec_data)

    return render(
        request=request,
        template_name='graph_explorer/_sheet_detail.html',
        context={
            'app': app,
            'country_flag': get_country_flag(app.country_code),
            'detail_sections': detail_sections,
            'resolved_errors': resolve_alerts(app.validation_errors, ui_strings, app.country_code),
            'resolved_warnings': resolve_alerts(app.rule_warnings, ui_strings, app.country_code),
            'ui': ui_strings
        }
    )


def app_cards_view(request, sheet_id):
    """Returns the Validation and Warning cards for a specific application."""
    app = get_object_or_404(Application, sheet_id=sheet_id)

    # Get 2D UI Strings for THIS specific application's country
    browser_lang = get_language()
    ui_strings = get_ui_strings(browser_lang, app.country_code)

    # Format the "Selected" string here in Python
    selected_template = ui_strings.get("CARD_SELECTED", "Selected: {req_num}")
    ui_strings["CARD_SELECTED"] = selected_template.format(req_num=app.request_number)

    return render(
        request=request,
        template_name='graph_explorer/_app_cards.html',
        context={
            'app': app,
            'ui': ui_strings,
            'resolved_errors':   resolve_alerts(app.validation_errors, ui_strings, app.country_code),
            'resolved_warnings': resolve_alerts(app.rule_warnings, ui_strings, app.country_code),
            'oob': True
        }
    )


def graph_data_view(request, sheet_id):
    """
    Calculates the 2-hop graph (Root Sheet -> Entities -> Connected Sheets)
    and returns Vis.js formatted JSON.
    Only includes entities that are shared with at least one other sheet.
    """
    try:
        root_app = Application.objects.get(sheet_id=sheet_id)
    except Application.DoesNotExist:
        return JsonResponse({"error": "Sheet not found"}, status=404)

    nodes = []
    edges = []
    node_ids = set()
    edge_map = set()

    def add_node(node_id, label, group, title=""):
        if node_id not in node_ids:
            node_data = {"id": node_id, "label": label, "group": group}
            # ONLY add the title key if it's not empty!
            if title:
                node_data["title"] = title
            nodes.append(node_data)
            node_ids.add(node_id)

    # Update helper to accept arrow direction
    def add_edge(from_id, to_id, title="", arrows="to"):
        edge_tuple = (from_id, to_id)
        if edge_tuple not in edge_map:
            edges.append({"from": from_id, "to": to_id, "arrows": arrows, "title": title})
            edge_map.add(edge_tuple)

    # Fetch UI strings
    browser_lang = get_language()
    ui_strings = get_ui_strings(browser_lang)

    # Add Root Sheet Node (Multi-line label using \n)
    root_node_id = f"sheet_{root_app.sheet_id}"
    root_label = _format_sheet_label(root_app, ui_strings)

    root_title = ui_strings.get("GRAPH_ROOT_TITLE", "")
    linked_title = ui_strings.get("GRAPH_LINKED_TITLE", "")
    linked_via = ui_strings.get("GRAPH_LINKED_VIA", "")

    add_node(root_node_id, root_label, "Root_Sheet", root_title)

    # Get 1st hop edges (to get source_field) and entities
    root_edges = UsesIdentifier.objects.filter(application=root_app).select_related('entity')

    for u_edge in root_edges:
        entity = u_edge.entity

        # Check 2nd hop (Other Sheets)
        connected_apps = entity.applications.exclude(sheet_id=root_app.sheet_id)

        # Only add the entity and the root->entity edge if it is shared
        if not connected_apps.exists():
            continue

        # Add Entity Node
        ent_node_id = f"ent_{entity.id}"

        # Truncate label for the canvas
        if len(entity.value) > 20:
            display_label = entity.value[:17] + "..."
            node_title = entity.value  # Only set title if truncated
        else:
            display_label = entity.value
            node_title = ""

        # Uppercase the entity type to match JS groups (e.g., 'VAT', 'TIN')
        group_name = entity.entity_type.upper()
        add_node(ent_node_id, display_label, group_name, node_title)

        root_context = _get_translated_field_context(u_edge.source_field, root_app.country_code)
        # Edge: Root Sheet -> Shared Entity
        add_edge(root_node_id, ent_node_id, f"{linked_via}:\n{root_context}", arrows="")

        # Add connected sheets (Multi-line label using \n)
        for conn_app in connected_apps:
            app_node_id = f"sheet_{conn_app.sheet_id}"
            conn_label = _format_sheet_label(conn_app, ui_strings)

            add_node(app_node_id, conn_label, "Linked_Sheet", linked_title)

            # Get the source field from the linked sheet's edge
            conn_u_edge = UsesIdentifier.objects.filter(application=conn_app, entity=entity).first()
            conn_context = _get_translated_field_context(conn_u_edge.source_field, conn_app.country_code) if conn_u_edge else "Unknown"

            # Edge: Shared Entity -> Connected Sheet (Keep arrows="to" so it points to the Linked Sheet)
            add_edge(ent_node_id, app_node_id, f"{linked_via}:\n{conn_context}", arrows="to")

    return JsonResponse({"nodes": nodes,"edges": edges})