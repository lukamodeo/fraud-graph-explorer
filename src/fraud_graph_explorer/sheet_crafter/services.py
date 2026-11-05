# src/fraud_graph_explorer/sheet_crafter/services.py

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
import re
import base64
import hashlib
import mimetypes
import codicefiscale

from typing import cast, Literal
from xhtml2pdf import pisa
from django.conf import settings
from fraud_graph_explorer.domain_schema import split_italian_full_name, FIELDS, SECTIONS, PDF
from .seed_data import get_random_profile, get_random_data


def _calculate_italian_tin(fullname: str, sex: str, dob: str, birthplace: str) -> str:
    """
    Calculates a valid Italian Codice Fiscale using python-codicefiscale.
    Assumes name format is "First Last"
    dob format: YYYY-MM-DD
    birthplace: 4-char code (e.g., H501 for Rome)
    """
    if not all([fullname, sex, dob, birthplace]):
        return "MISSING_DATA"

    try:
        # Use the intelligent splitter
        first_name, last_name = split_italian_full_name(fullname)

        # Cast the sex variable to satisfy the Literal type hint
        gender_val = cast(Literal["m", "M", "f", "F"], sex.upper())

        # Call the library with the EXACT parameter names
        cf = codicefiscale.encode(
            lastname=last_name,
            firstname=first_name,
            gender=gender_val,
            birthdate=dob,
            birthplace=birthplace
        )
        return cf or "CALC_FAILED"

    except ValueError as e:
        # Handle cases where the name couldn't be split
        print(f"Name split error: {e}")
        return "INVALID_NAME_FORMAT"
    except Exception as e:
        # If the library throws an error (e.g., invalid birthplace code)
        print(f"Codice Fiscale Error: {e}")
        return "CALC_ERROR"

def _calculate_french_tin(fullname: str, sex: str, dob: str, birthplace: str) -> str:
    """
    Calculates a valid French NIR (Social Security Number).
    Uses MD5 hash of the fullname to generate a deterministic 3-digit serial number.
    dob format: YYYY-MM-DD
    birthplace format: 5 chars (2 Dept + 3 Town) e.g., '75123'
    """
    if not all([fullname, sex, dob, birthplace]):
        return "MISSING_DATA"

    # Sex (1: Male, 2: Female)
    sex_code = '1' if sex.upper() == 'M' else '2'

    # Year (2 digits)
    year = dob[2:4]

    # Month (2 digits)
    month = dob[5:7]

    # Parse the 8-character birthplace string
    if len(birthplace) != 5 or not birthplace.isdigit():
        return "INVALID_BIRTHPLACE_FORMAT"

    dept = birthplace[0:2]
    town_code = birthplace[2:5]

    # DETERMINISTIC SERIAL NUMBER (Hash the fullname to 3 digits)
    # This ensures different names yield different TINs, but recalculation is stable.
    name_hash = hashlib.md5(fullname.encode()).hexdigest()
    serial_int = int(name_hash, 16) % 1000 # Modulo 1000 gives us exactly 3 digits (000-999)
    serial = f"{serial_int:03d}"

    # Construct the 13-digit NIR
    nir_13_str = f"{sex_code}{year}{month}{dept}{town_code}{serial}"
    nir_13 = int(nir_13_str)

    # Control Key (2 digits)
    control_key = 97 - (nir_13 % 97)
    control_str = f"{control_key:02d}"

    return f"{nir_13_str}{control_str}"


def get_calculated_tin(country_code: str, data: dict) -> str:
    """Router function to call the right TIN calculator.

    Note: mutates `data` in place, writing back the resolved dob/birthplace
    values (fallbacks and normalizations). Callers can read data['dob'] and
    data['birthplace'] after the call to get the actual values used.
    """
    fullname = data.get('fullname', '')
    sex = data.get('sex', '') or 'M'
    dob = data.get('dob', '')
    birthplace = data.get('birthplace', '')

    # Lazy-load a profile ONLY if we need to fix dob or birthplace
    _fallback_profile = None

    if not dob:
        _fallback_profile = get_random_profile(country_code)
        dob = _fallback_profile['birthdate']
        data['dob'] = dob               # <-- NEW: write back fallback

    # Validate birthplace format per country
    if country_code == 'IT':
        if not re.match(r'^[A-Z]\d{3}$', (birthplace or '').upper()):
            if not _fallback_profile:
                _fallback_profile = get_random_profile('IT')
            birthplace = _fallback_profile['birthplace']
            data['birthplace'] = birthplace   # <-- NEW: write back fallback
        else:
            birthplace = birthplace.upper()
            data['birthplace'] = birthplace   # <-- NEW: write back normalized
    elif country_code == 'FR':
        if not re.match(r'^\d{5}$', birthplace or ''):
            if not _fallback_profile:
                _fallback_profile = get_random_profile('FR')
            birthplace = _fallback_profile['birthplace']
            data['birthplace'] = birthplace   # <-- NEW: write back fallback

    if country_code == 'IT':
        return _calculate_italian_tin(fullname, sex, dob, birthplace)
    elif country_code == 'FR':
        return _calculate_french_tin(fullname, sex, dob, birthplace)
    else:
        return "CALC_NOT_SUPPORTED"


def generate_dynamic_initial_data(country_code: str) -> dict:
    """
    Dynamically generates initial form data based on the FIELDS schema.
    Uses 'calc_fields' to ensure relational consistency for groups.
    """
    initial_data = {}
    generated_keys = set()  # To track fields already filled via profiles
    used_fullnames = set()  # To track names in the same form

    # Process Relational Groups (Fields with 'calc_fields')
    for internal_name, config in FIELDS.items():
        if "calc_fields" in config:

            field_map = config["calc_fields"]

            # Fetch ONE profile, ensuring the fullname is unique for this PDF
            # We try up to 10 times to find a unique name (highly likely with 128 combos)
            # Fallback: if we fail 10 times, we just accept the duplicate to prevent infinite loops
            attempts = 0
            profile = {}
            while attempts < 10:
                profile = get_random_profile(country_code)
                if profile["fullname"] not in used_fullnames:
                    used_fullnames.add(profile["fullname"])
                    break
                attempts += 1


            # Distribute the profile data to the exact internal names
            initial_data[field_map["fullname"]] = profile["fullname"]
            initial_data[field_map["sex"]] = profile["sex"]
            initial_data[field_map["dob"]] = profile["birthdate"]
            initial_data[field_map["birthplace"]] = profile["birthplace"]

            # If the country supports algorithmic TINs, calculate it dynamically!
            if country_code in ['IT', 'FR']:
                initial_data[field_map["tin"]] = get_calculated_tin(country_code, {
                    'fullname': profile["fullname"],
                    'sex': profile["sex"],
                    'dob': profile["birthdate"],
                    'birthplace': profile["birthplace"]
                    })
            else:
                # Fallback to the random TIN from the seed data for DE, ES, GB
                initial_data[field_map["tin"]] = profile["tin"]

            # Mark these as done so they aren't overwritten in next step
            generated_keys.update(field_map.values())

    # Process Standalone Fields
    for internal_name, config in FIELDS.items():
        if internal_name not in generated_keys:
            fake_type = config.get("fake_type")
            if fake_type:
                # Pass **initial_data so get_random_data can read the company_name!
                initial_value = get_random_data(country_code, fake_type, **initial_data)
                if fake_type == "amount" and country_code == "GB":
                    initial_value = initial_value.replace('.', ',')
                initial_data[internal_name] = initial_value

    initial_data['country_code'] = country_code

    return initial_data


def generate_pdf_sheet(country_code: str, form_data: dict, filepath: str):
    """
    Generates a PDF using xhtml2pdf with HTML support and old version CSS support.
    """

    # Calculate path to the image and convert to Base64
    image_filename = "pdf-head-v4.png"
    image_path = os.path.join(settings.BASE_DIR, 'static', 'img', image_filename)

    base64_src = ""
    if os.path.exists(image_path):
        # Guess the MIME type dynamically (e.g., 'image/png' or 'image/jpeg')
        mime_type, _ = mimetypes.guess_type(image_path)
        # Fallback to png if the extension is weird or missing
        if not mime_type:
            mime_type = "image/png"

        # Read and encode the file
        with open(image_path, "rb") as img_file:
            base64_bytes = base64.b64encode(img_file.read())
            base64_string = base64_bytes.decode('utf-8')

        # Construct the full src string
        base64_src = f"data:{mime_type};base64,{base64_string}"

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
                margin-top: 12px;
                margin-bottom: 4px;
            }}
            h2 {{ 
                font-size: 14px; 
                color: #ffffff; 
                background-color: #44596e; 
                padding-top: 12px;
                padding-left: 16px;
                padding-bottom: 2px;
                margin-bottom: 0;
                margin-top: 0; 
            }}
            table {{ 
                width: 100%; 
                margin-bottom: 20px; 
            }}
            td {{ 
                border: 1px solid #dddddd; 
                padding-top: 6px;
                padding-left: 8px;
                padding-bottom: 2px;
                vertical-align: top; 
            }}
            td.label {{ 
                width: 55%; 
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

    # Inject the PDF head using the Base64 string
    if base64_src:
        html_content += f'<div class="page-head"><img src="{base64_src}" alt="Bank"></div>\n'

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

    # For debug only
    # with open(f"{filepath}.html", "w") as output_file_html:
    #     output_file_html.write(html_content)

    # Open a file and let pisa write the PDF directly to it
    with open(filepath, "wb") as output_file:
        pisa_status = pisa.CreatePDF(html_content, dest=output_file)

    if pisa_status.err:
        raise Exception("PDF generation failed")
