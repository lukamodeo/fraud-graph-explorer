# src/fraud_graph_explorer/sheet_crafter/services.py
import os
import uuid
#from markdown_pdf import MarkdownPdf, Section
from xhtml2pdf import pisa
from fraud_graph_explorer.graph_explorer.ingestion_schema import FIELDS, SECTIONS, PDF
from .seed_data import get_random_profile

def generate_dynamic_initial_data(country_code: str) -> dict:
    """
    Dynamically generates initial form data based on the FIELDS schema.
    Uses 'calc_fields' to ensure relational consistency for groups.
    """
    initial_data = {'country_code': country_code}
    generated_keys = set()  # Tracks fields we already filled via a group

    # 1. Process Relational Groups (Fields with 'calc_fields')
    for internal_name, config in FIELDS.items():
        if "calc_fields" in config:
            # Fetch ONE profile for this whole group
            profile = get_random_profile(country_code)
            field_map = config["calc_fields"]

            # Distribute the profile data to the exact internal names
            initial_data[field_map["name"]] = profile["name"]
            initial_data[field_map["sex"]] = profile["sex"]
            initial_data[field_map["dob"]] = profile["birthdate"]
            initial_data[field_map["birthplace"]] = profile.get("birthplace", "XXXX")
            initial_data[field_map["tin"]] = profile["tin"]

            # Mark these as done so they aren't overwritten in step 2
            generated_keys.update(field_map.values())

    # 2. Process Standalone Fields (Fields without 'calc_fields')
    # Define how to generate standalone fake types
    def generate_standalone(fake_type):
        if fake_type == "request_id":
            return f"{country_code.upper()}-{uuid.uuid4().hex[:6].upper()}"
        elif fake_type == "location":
            return "Roma"
        elif fake_type == "amount":
            return "35.000"
        elif fake_type == "company_name":
            return f"Acme Industries {country_code}"
        elif fake_type == "vat":
            return get_random_profile(country_code)['vat']
        elif fake_type == "email":
            return "pippo@poppi.it"
        elif fake_type == "phone":
            return "+39123456789"
        return ""

    for internal_name, config in FIELDS.items():
        if internal_name not in generated_keys:
            fake_type = config.get("fake_type")
            if fake_type:
                initial_data[internal_name] = generate_standalone(fake_type)

    return initial_data




# def generate_dynamic_initial_data(country_code: str) -> dict:
#     """
#     Reads the schema and generates initial form data dynamically.
#     """
#     profile = get_random_profile(country_code)
#     initial_data = {'country_code': country_code}
#
#     # Map fake_types to the profile data or generation logic
#     fake_map = {
#         "request_id": f"REQ-{uuid.uuid4().hex[:6].upper()}",
#         "company_name": f"Acme Industries {country_code}",
#         "vat": profile['vat'],
#         "name": profile['name'],
#         "birthdate": profile['birthdate'],
#         "tin": profile['tin'],
#         "birthplace": profile.get('birthplace', 'XXXX')  # <--- ADD THIS
#     }
#
#     for internal_name, config in FIELDS.items():
#         fake_type = config.get("fake_type")
#         if fake_type and fake_type in fake_map:
#             initial_data[internal_name] = fake_map[fake_type]
#
#     return initial_data


# src/fraud_graph_explorer/sheet_crafter/services.py



def generate_pdf_sheet(country_code: str, form_data: dict, filepath: str):
    """
    Generates a PDF using xhtml2pdf with HTML support and old version CSS support.
    """

    # Start HTML document with embedded CSS
    html_content = f"""
    <!DOCTYPE html>
    <html lang="{country_code.lower()}">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ 
                font-family: Verdana, Arial, sans-serif; 
                font-size: 12px; 
                color: #333333; 
            }}
            h1 {{ 
                font-size: 20px; 
                text-align: center; 
                color: #2c3e50; 
            }}
            h2 {{ 
                font-size: 14px; 
                color: #ffffff; 
                background-color: #44596e; 
                padding-top: 12px;
                padding-left: 16px;
                padding-bottom: 2px;
                margin-bottom: 0; 
            }}
            table {{ 
                width: 100%; 
                margin-bottom: 20px; 
                border-spacing: 0;
            }}
            td {{ 
                border: 1px solid #dddddd; 
                padding-top: 8px;
                padding-left: 8px;
                padding-bottom: 4px;
                vertical-align: top; 
            }}
            td.label {{ 
                width: 40%; 
                font-weight: bold; 
                background-color: #f9f9f9; 
            }}
            tr.group-header td {{ 
                background-color: #ecf0f1; 
                font-weight: bold; 
                font-style: italic; 
                border-bottom: 2px solid #34495e; 
            }}
            div.footer {{ 
                text-align: center; 
                font-size: 0.9rem; 
            }}
        </style>
    </head>
    <body>
    """

    # Main Document Title
    title = f'{PDF["header"][country_code]} ({country_code})'
    html_content += f"<h1>{title}</h1>\n"

    # Loop through sections and fields
    for section in SECTIONS:
        section_title = section["labels"].get(country_code, section["labels"]["GB"])
        html_content += f"<h2>{section_title}</h2>\n"

        html_content += "<table>\n"
        for field_name in section.get("fields", []):
            field_config = FIELDS.get(field_name)

            if not field_config or field_config.get("hidden"):
                continue

            label = field_config["labels"].get(country_code, field_config["labels"]["GB"])
            value = form_data.get(field_name, "")
            html_content += f'<tr><td class="label">{label}</td><td>{value}</td></tr>\n'
        html_content += "</table>\n"

    html_content += f'<div class="footer">{PDF["footer"][country_code]}</div>'
    html_content += "</body></html>"

    # Generate the PDF using xhtml2pdf
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # with open(f"{filepath}.html", "w") as output_file_html:
    #     output_file_html.write(html_content)

    # Open a file and let pisa write the PDF directly to it
    with open(filepath, "wb") as output_file:
        pisa_status = pisa.CreatePDF(html_content, dest=output_file)

    if pisa_status.err:
        raise Exception("PDF generation failed")


# def generate_pdf_sheet_old1(country_code: str, form_data: dict, filepath: str):
#     """
#     Generates a PDF using the ingestion schema and the form data.
#     """
#     title = f"{PDF['header'][country_code]} ({country_code})"
#     #md_content = f"# Loan Application Sheet ({country_code})\n\n"
#     #md_content = f"<h3>{PDF['header'][country_code]} ({country_code})</h3>"
#     md_content = f"# {title}\n\n"
#
#     # fake_data = {
#     #     "request_number": form_data.get('request_number', ''),
#     #     "company_name": form_data.get('company_name', ''),
#     #     "company_vatn_taxc": form_data.get('company_vatn_taxc', ''),
#     #     "taxcode_legal_representative": form_data.get('taxcode_legal_representative', ''),
#     #     }
#
#     for section in SECTIONS:
#         section_title = section["labels"].get(country_code, section["labels"]["GB"])
#         md_content += f"## {section_title}\n\n"
#
#         # 1. Start an HTML table with a little inline CSS for clean borders
#         md_content += '<table style="width: 100%; border-collapse: collapse;">\n'
#
#         for field_name in section["fields"]:
#             field_config = FIELDS.get(field_name)
#             if not field_config:
#                 continue
#
#             # 1. SKIP HIDDEN FIELDS - Do not print on the PDF
#             if field_config.get("hidden"):
#                 continue
#
#             label = field_config["labels"].get(country_code, field_config["labels"]["GB"])
#             # form_data keys map directly to internal_name
#             value = form_data.get(field_name, "")
#
#             # 2. Add standard HTML rows.
#             # We can make the left column bold and add borders directly in the HTML
#             md_content += (
#                 f'<tr>'
#                 f'<td style="border: 1px solid #ccc; padding: 8px; width: 65%; font-weight: bold;">{label}</td>'
#                 f'<td style="border: 1px solid #ccc; padding: 8px; width: 35%;">{value}</td>'
#                 f'</tr>\n'
#             )
#
#         # 3. Close the HTML table
#         md_content += '</table>\n\n'
#
#     md_content += f"<p style='text-align: center; font-size: 0.5rem;'>{PDF['footer'][country_code]} ({country_code})</p>"
#
#
#     # Generate the PDF (rest of the function remains the same)
#     os.makedirs(os.path.dirname(filepath), exist_ok=True)
#     pdf = MarkdownPdf() #toc_level=2)
#     pdf.add_section(Section(md_content))
#     pdf.meta = {"title": title}
#     pdf.save(filepath)



# def generate_pdf_sheet_old(country_code: str, form_data: dict, filepath: str):
#     """
#     Generates a PDF using the ingestion schema and the form data.
#     """
#     # 1. Add a Level 1 Header at the very top!
#     md_content = f"# Loan Application Sheet ({country_code})\n\n"
#
#     # Map form fields to the internal names expected by the schema
#     fake_data = {
#         "request_number": form_data.get('request_number', ''),
#         "company_name": form_data.get('company_name', ''),
#         "company_vatn_taxc": form_data.get('company_vatn_taxc', ''),
#         "taxcode_legal_representative": form_data.get('taxcode_legal_representative', ''),
#         # We can add legal_rep_name and dob to the schema later if needed,
#         # but for now we'll just include them as extra rows in the table manually if desired.
#     }
#
#     # Build Markdown using the localized schema
#     for section in SECTIONS:
#         # Get the localized section header (e.g., "UNTERNEHMENSPROFIL")
#         section_title = section["labels"].get(country_code, section["labels"]["GB"])
#
#         # These are Level 2 Headers
#         md_content += f"## {section_title}\n\n"
#
#         # Start the two-column markdown table
#         #md_content += "| Field | Data |\n|---|---|\n"
#         md_content += "| &nbsp; | &nbsp; |\n|---|---|\n"
#
#         for field_name in section["fields"]:
#             # Get the localized field label (e.g., "UST-IDNR - STEUERNUMMER")
#             label = FIELDS[field_name]["labels"].get(country_code, FIELDS[field_name]["labels"]["GB"])
#             value = fake_data.get(field_name, "")
#             md_content += f"| {label} | {value} |\n"
#
#         md_content += "\n"  # Spacing between sections
#
#     # Generate the PDF
#     os.makedirs(os.path.dirname(filepath), exist_ok=True)
#
#     # toc_level=2 is now perfectly valid because we have a # and ## in the document
#     pdf = MarkdownPdf(toc_level=2)
#     pdf.add_section(Section(md_content))
#     pdf.meta = {"title": f"Loan Application - {country_code}"}
#     pdf.save(filepath)