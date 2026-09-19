# src/fraud_graph_explorer/graph_explorer/services.py
from .models import Application, Entity
from .ingestion_schema import FIELDS, SECTIONS


def build_reverse_lookup_map():
    """
    Creates a dictionary like:
    {"ANTRAGSNUMMER": {"internal_name": "numero_richiesta", "tags": ["Sheet"]}, ...}
    for all languages.
    """
    lookup = {}
    for internal_name, config in FIELDS.items():
        for lang, label in config["labels"].items():
            lookup[label] = {
                "internal_name": internal_name,
                "tags": config["tags"]
                }
    return lookup


# Build this once when the module loads
REVERSE_LOOKUP = build_reverse_lookup_map()


def ingest_pdf_data(raw_pdf_data: dict, country_code: str, pdf_file_path: str):
    """
    raw_pdf_data: {"ANTRAGSNUMMER": "12345", "FIRMA DES ANTRAGSTELLERS": "Siemens"}
    """
    app = Application.objects.create(
        country_code=country_code,
        applicant_name="Placeholder",
        pdf_file=pdf_file_path
        )

    # Iterate over the extracted PDF key-value pairs
    for raw_label, value in raw_pdf_data.items():
        # Clean up any whitespace from PDF extraction
        clean_label = raw_label.strip()

        # Use the reverse lookup to find the business logic
        field_info = REVERSE_LOOKUP.get(clean_label)

        if not field_info:
            continue  # Ignore fields not in our schema

        internal_name = field_info["internal_name"]
        tags = field_info["tags"]

        # Assign to Application model if it has a "Sheet" tag
        if "Sheet" in tags:
            if hasattr(app, internal_name):
                setattr(app, internal_name, value)

        # Create Graph Entities for other tags (VAT, TIN, COMPANY)
        entity_types = [t for t in tags if t != "Sheet"]
        for e_type in entity_types:
            entity, _ = Entity.objects.get_or_create(
                entity_type=e_type,
                value=value
                )
            app.entities.add(entity)

    app.save()
    return app