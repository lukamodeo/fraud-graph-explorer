# src/fraud_graph_explorer/graph_explorer/services.py

import io
import ipaddress
import pdfplumber
from decimal import Decimal, InvalidOperation
from django.core.files.base import ContentFile

from .models import Application, Entity, UsesIdentifier, Blacklist
from .validation_engine import ValidationRegistry, RuleRegistry
from fraud_graph_explorer.domain_schema import FIELDS, SECTION_LOOKUP, SECTIONS_BY_INTERNAL, INTL_PHONE_PREFIX, SECTION_COUNTRY_LOOKUP



def _normalize_value(raw_value: str, config: dict, country_code: str):
    """
    Helper function to normalize extracted values based on their tags and type.
    Returns the normalized value, or None if a Decimal fails to parse.
    """
    norm_value = raw_value.strip()
    tags = config.get("tags", [])
    field_type = config.get("type")

    # Handle Empty Strings early
    if not norm_value:
        # Django's DecimalField requires None, not ""
        return None if field_type == "decimal" else ""

    # Tag-based Normalization
    if "TIN" in tags:
        norm_value = norm_value.upper().replace(" ", "").replace("-", "")

    elif "VAT" in tags or "IBAN" in tags:
        norm_value = norm_value.upper().replace(" ", "").replace("-", "")
        # If it doesn't start with letters, prepend the country code
        if not norm_value[:2].isalpha():
            norm_value = f"{country_code}{norm_value}"

    elif "EMAIL" in tags:
        norm_value = norm_value.replace(" ", "").lower()

    elif "PHONE" in tags:
        norm_value = norm_value.replace(" ", "").replace("-", "").replace("/", "")
        # If it doesn't start with international prefix, prepend it based on country code
        if not norm_value.startswith('+'):
            prefix = INTL_PHONE_PREFIX.get(country_code, '')
            norm_value = f"{prefix}{norm_value}"

    elif "IP" in tags:
        # Zero-pad IPv4 octets: 192.168.0.3 -> 192.168.000.003
        try:
            # Validate it's a real IP first
            ip_obj = ipaddress.IPv4Address(norm_value)
            parts = str(ip_obj).split(".")
            norm_value = ".".join([p.zfill(3) for p in parts])
        except ipaddress.AddressValueError:
            # If it's invalid, leave it as is.
            # The validation engine will catch it and log an error!
            pass

    # Normalize Names, Companies, and Locations
    elif "FULLNAME" in tags or "COMPANY" in tags or "LOCATION" in tags:
        # .split() without arguments splits on ANY whitespace (spaces, tabs, newlines)
        # " ".join() puts it back together with a single clean space
        norm_value = " ".join(norm_value.split())

        # Optional: You can also force Title Case here to catch "mario rossi" vs "Mario Rossi"
        norm_value = norm_value.title()

    # Type-based Normalization (Decimal)
    if field_type == "decimal":
        try:
            clean_val = norm_value.replace("€", "").strip()
            if not clean_val:
                return None
            # Assume EU format ("280.000" -> 280000.00, "280,50" -> 280.50)
            clean_val = clean_val.replace(".", "").replace(",", ".")
            return Decimal(clean_val)
        except (InvalidOperation, ValueError):
            return None

    return norm_value

def ingest_pdf(pdf_bytes: bytes, country_code: str, file_name: str, overwrite: bool = False):
    """
    Parses a PDF from memory, normalizes data, runs validation/rules,
    and creates Graph nodes/edges.
    """
    extracted_data = []  # List of tuples: (internal_name, raw_value, config)

    # ==========================================
    # STEP 1: Extraction (Section-Aware State Machine)
    # ==========================================
    try:
        # Read PDF directly from bytes in memory
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:

            # --- AUTO-DETECT COUNTRY FROM SECTIONS ---
            # Scan the first page for any known localized section headers
            first_page_text = pdf.pages[0].extract_text() or ""
            for header, detected_cc in SECTION_COUNTRY_LOOKUP.items():
                if header in first_page_text:
                    country_code = detected_cc
                    break
            # ---------------------------------------------

            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue

                lines = text.split('\n')

                current_section = None
                expected_fields_queue = []

                for line in lines:
                    line = line.strip()
                    if not line:
                        continue

                    # Check for Section Change
                    if line in SECTION_LOOKUP:
                        current_section = SECTION_LOOKUP[line]
                        expected_fields_queue = list(SECTIONS_BY_INTERNAL[current_section].get("fields", []))
                        print(f"\n[STATE] Found Section: {current_section}. Expected fields: {expected_fields_queue}")
                        continue

                    # Check for Field
                    if current_section and expected_fields_queue:
                        for internal_name in expected_fields_queue:
                            config = FIELDS.get(internal_name)
                            if not config:
                                continue

                            matched_label = None
                            for lang, label in config.get("labels", {}).items():
                                if line.startswith(label):
                                    matched_label = label
                                    break

                            if matched_label:
                                # Extract the value
                                raw_value = line[len(matched_label):].strip()
                                # FIX 1: Only strip colons, leave dashes (minus signs) alone!
                                if raw_value.startswith(':'):
                                    raw_value = raw_value[1:].strip()

                                # We ALWAYS append, even if empty, so the validation engine can catch missing required fields!
                                print(f"  [MATCH] '{line}' -> Field: {internal_name}, Value: {raw_value}")
                                extracted_data.append((internal_name, raw_value, config))
                                expected_fields_queue.remove(internal_name)
                                break  # Move to the next line

    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return None, "parse_error", None

    # ==========================================
    # ABORT IF NOT A VALID APPLICATION SHEET
    # ==========================================
    # If the state machine didn't find any fields, it's not a loan application!
    # Also check if it has the core required field (request_number)
    if not extracted_data or "request_number" not in [item[0] for item in extracted_data] :
        print("Ingestion aborted: No recognizable fields found in PDF or missing core 'request_number' field.")
        return None, "invalid_sheet", None


    # ==========================================
    # PRE-INGESTION DUPLICATE CHECK
    # ==========================================
    # Look for the request_number in our extracted_data list of tuples
    req_number_config = FIELDS.get("request_number", {})
    is_unique = req_number_config.get("unique_id", False)

    if is_unique:
        for internal_name, raw_value, config in extracted_data:
            if internal_name == "request_number":
                # Check if an application with this request number already exists
                existing_app = Application.objects.filter(request_number=raw_value).first()
                if existing_app:
                    if not overwrite:
                        print(f"Duplicate detected: {raw_value}")
                        return None, "duplicate", existing_app # Return the existing app!
                    else:
                        # User confirmed overwrite! Delete old record.
                        existing_app.delete()
                break

    # ==========================================
    # STEP 2: Normalization (Context-Aware)
    # ==========================================
    raw_data = {}           # Only .strip() applied (Forensic evidence)
    normalized_data = {}    # Cleaned for graph linking and database

    for internal_name, raw_value, config in extracted_data:
        raw_data[internal_name] = raw_value

        norm_value = _normalize_value(raw_value, config, country_code)

        normalized_data[internal_name] = norm_value


    # ==========================================
    # STEP 3 & 4: Validations and Business Rules
    # ==========================================
    app = Application(
        country_code=country_code,
        file_name=file_name,
        validation_errors=[],
        rule_warnings=[]
    )

    validation_errors_list = []
    rule_warnings_list = []

    # Context required by the dynamic rules engine
    schema_context = {"FIELDS": FIELDS}

    # Fetch blacklists from database building a dictionary like: {"vat": {"IT123", "IT456"}, "tin": {"BNCFNC..."}}
    blacklists = {}
    for item in Blacklist.objects.all():
        # Convert DB Enum (e.g., "VAT") to lowercase string ("vat") to match tag logic
        bl_type = item.entity_type.lower()
        if bl_type not in blacklists:
            blacklists[bl_type] = set()
        blacklists[bl_type].add(item.value)

    # Track sheet-level rules so they only run ONCE per document
    seen_sheet_rules = set()

    for internal_name, norm_value in normalized_data.items():
        config = FIELDS.get(internal_name, {})
        raw_val = raw_data.get(internal_name, "")

        # Implicit "required" Validation
        if config.get("required") and not raw_val:
            validation_errors_list.append({
                "type_key": "TYPE_REQUIRED",
                "reason_key": "REASON_REQUIRED",
                "severity": "critical",
                "value": norm_value,
                "raw_value": raw_val,
                "field": internal_name,
                "validation_id": "required_implicit"
            })
            continue  # Skip other checks if it's completely missing

        # Explicit Validations
        for validation_id in config.get("validations", []):
            results = ValidationRegistry.run(
                item_id=validation_id,
                raw_value=raw_val,
                norm_value=norm_value,
                config=config,
                all_data=normalized_data,
                country_code=app.country_code,
                internal_name=internal_name
            )
            validation_errors_list.extend(results)

        # Explicit Rules (Fully Dynamic & Generic)
        for rule_id in config.get("rules", []):
            meta = RuleRegistry.get_meta(rule_id)

            if not meta:
                continue    # Unknown rule type, skip silently

            # If it's a sheet-level rule, ensure it only runs once
            if meta.get("scope") == "sheet":
                if rule_id in seen_sheet_rules:
                    continue
                seen_sheet_rules.add(rule_id)

            # Execute the rule
            results = RuleRegistry.run(
                item_id=rule_id,
                raw_value=raw_val,
                norm_value=norm_value,
                config=config,
                all_data=normalized_data,
                raw_data=raw_data,
                schema=schema_context,
                blacklists=blacklists,
                internal_name=internal_name,
                country_code=app.country_code
            )

            # Intercept dynamic type_key overrides
            for r in results:
                if "type_key_override" in r:
                    r["type_key"] = r.pop("type_key_override")
                rule_warnings_list.append(r)

    # ==========================================
    # STEP 5: Graph Population & Save
    # ==========================================
    app.validation_errors = validation_errors_list
    app.rule_warnings = rule_warnings_list
    app.has_validation_errors = len(validation_errors_list) > 0
    app.has_rule_warnings = len(rule_warnings_list) > 0
    # Save the base Application object first so it has a PK for relationships
    app.save()

    # Create Graph Entities and Edges
    for internal_name, norm_value in normalized_data.items():
        config = FIELDS[internal_name]
        tags = config.get("tags", [])
        raw_val = raw_data.get(internal_name, "")

        # Save to Application model if "Sheet" tag is present
        if "Sheet" in tags and hasattr(app, internal_name):
            setattr(app, internal_name, norm_value)

        # Create Graph Entities (Identifier Vertices) for other tags
        entity_types = [t for t in tags if t != "Sheet"]
        for e_type in entity_types:
            if not norm_value:
                continue

            # Create/Get Entity using the NORMALIZED value (for perfect graph linking)
            entity, _ = Entity.objects.get_or_create(
                entity_type=e_type,
                value=norm_value
            )

            # Create Edge using the RAW value and specific source_field (for forensic evidence)
            UsesIdentifier.objects.get_or_create(
                application=app,
                entity=entity,
                source_field=internal_name, # <-- Added to the lookup!
                defaults={
                    'original_value': raw_val  # Saved on the edge!
                }
            )

    # Save the PDF bytes to the FileField
    app.pdf_file.save(file_name, ContentFile(pdf_bytes), save=False)

    # Final save to persist any updated Sheet attributes
    app.save()

    return app, None, None

def annotate_has_links(apps_qs):
    """
    Attach a `has_links` boolean attribute to each Application in `apps_qs`,
    indicating whether at least one OTHER application shares an Entity via
    UsesIdentifier edges (either on this page or elsewhere in the DB).

    Uses a Python-side computation rather than ORM annotation, because
    Django's compiler mishandles the double OuterRef('pk') correlation
    needed for this particular self-join through UsesIdentifier.

    Returns a list of Application instances (queryset is force-evaluated).
    """
    apps = list(apps_qs)
    if not apps:
        return apps

    app_pks = [app.pk for app in apps]

    # Query 1: (app_pk, entity_pk) edges for the apps on this page
    my_edges = (
        UsesIdentifier.objects
        .filter(application_id__in=app_pks)
        .values_list('application_id', 'entity_id')
    )

    # Query 2: any OTHER edge pointing to one of those same entities
    app_to_entities = {}
    for app_pk, entity_pk in my_edges:
        app_to_entities.setdefault(app_pk, set()).add(entity_pk)

    all_my_entity_ids = set().union(*app_to_entities.values()) if app_to_entities else set()
    other_linked_entity_ids = set(
        UsesIdentifier.objects
        .filter(entity_id__in=all_my_entity_ids)
        .exclude(application_id__in=app_pks)
        .values_list('entity_id', flat=True)
    ) if all_my_entity_ids else set()

    # Intra-page links: two apps on this page sharing an entity
    intra_page_linked = set()
    for app_pk, ents in app_to_entities.items():
        for other_app_pk, other_ents in app_to_entities.items():
            if app_pk != other_app_pk and ents & other_ents:
                intra_page_linked.add(app_pk)

    for app in apps:
        app.has_links = (
            app.pk in intra_page_linked
            or bool(app_to_entities.get(app.pk, set()) & other_linked_entity_ids)
        )

    return apps