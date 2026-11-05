# src/fraud_graph_explorer/graph_explorer/domain_schema.py

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

from django.db import models

# Centralized Enums
class CountryCodes(models.TextChoices):
    ITALY = 'IT', 'Italy'
    GERMANY = 'DE', 'Germany'
    FRANCE = 'FR', 'France'
    SPAIN = 'ES', 'Spain'
    UK = 'GB', 'United Kingdom'


class EntityTypes(models.TextChoices):
    VAT = 'VAT', 'VAT Number'
    TIN = 'TIN', 'Tax ID Number'
    FULLNAME = 'FULLNAME', 'Full Name'
    IBAN = 'IBAN', 'IBAN Code'
    IP = 'IP', 'IPv4 Address'
    EMAIL = 'EMAIL', 'Email Address'
    PHONE = 'PHONE', 'Phone Number'
    COMPANY = 'COMPANY', 'Company Name'
    LOCATION = 'LOCATION', 'Location'


# Centralized Visual Metadata for Vis.js and the Legend
ENTITY_GRAPH_META = {
    EntityTypes.VAT.value: {'bs_icon': '\uf2da', 'css_icon': 'bi-credit-card-2-front', 'color': '#d4ae18', 'label_key': 'LEGEND_VAT'},
    EntityTypes.TIN.value: {'bs_icon': '\uf8c9', 'css_icon': 'bi-person-vcard', 'color': '#a09e16', 'label_key': 'LEGEND_TIN'},
    EntityTypes.IBAN.value: {'bs_icon': '\uf62e', 'css_icon': 'bi-bank', 'color': '#27ae60', 'label_key': 'LEGEND_IBAN'},
    EntityTypes.IP.value: {'bs_icon': '\uf3ef', 'css_icon': 'bi-globe2', 'color': '#7f8c8d', 'label_key': 'LEGEND_IP'},
    EntityTypes.COMPANY.value: {'bs_icon': '\uf87d', 'css_icon': 'bi-buildings', 'color': '#f39c12', 'label_key': 'LEGEND_COMPANY'},
    EntityTypes.LOCATION.value: {'bs_icon': '\uf3e8', 'css_icon': 'bi-geo-alt', 'color': '#ff2222', 'label_key': 'LEGEND_LOCATION'},
    EntityTypes.FULLNAME.value: {'bs_icon': '\uf4d4', 'css_icon': 'bi-person-bounding-box', 'color': '#2146b5', 'label_key': 'LEGEND_FULLNAME'},
    EntityTypes.EMAIL.value: {'bs_icon': '\uf84c', 'css_icon': 'bi-envelope-at', 'color': '#f1c40f', 'label_key': 'LEGEND_EMAIL'},
    EntityTypes.PHONE.value: {'bs_icon': '\uf655', 'css_icon': 'bi-sd-card', 'color': '#a12494f', 'label_key': 'LEGEND_PHONE'},
}


# Centralized Country Constants
INTL_PHONE_PREFIX = {
    'IT': '+39',
    'DE': '+49',
    'FR': '+33',
    'ES': '+34',
    'GB': '+44'
}

# FIELDS — the central schema dict.
#
# Tag conventions:
#   "Sheet" tag = field stored directly on Application model (legacy name).
#                 Other tags (VAT, TIN, IBAN, etc.) create Entity vertices.
FIELDS = {
    "request_number": {
        "unique_id": True,
        "type": "string",
        "tags": ["Sheet"],
        "list_view": True,
        "list_label": "COL_ID",
        "required": True,
        "max_length": 50,
        "fake_type": "id",
        "labels": {
            "IT": "N. DOMANDA",
            "DE": "ANTRAGS-NR.",
            "FR": "N° DE DEMANDE",
            "ES": "N.° DE SOLICITUD",
            "GB": "APPLICATION NO."
        }
    },
    "request_branch_location":{
        "type": "string",
        "tags": ["Sheet"],
        "max_length": 50,
        "fake_type": "location",
        "labels": {
            "IT": "SEDE DELLA FILIALE",
            "DE": "ORT DER FILIALE",
            "FR": "LOCALISATION DE L’AGENCE",
            "ES": "LOCALIDAD DE LA SUCURSAL",
            "GB": "BRANCH LOCATION"
        }
    },
    "request_amount":{
        "type": "decimal",
        "tags": ["Sheet"],
        "list_view": True,
        "list_label": "COL_AMOUNT",
        "required": True,
        "validations": ["numeric"],
        "rules": ["positive"],
        "max_length": 12,
        "fake_type": "amount",
        "labels": {
            "IT": "IMPORTO RICHIESTO",
            "DE": "BEANTRAGTER BETRAG",
            "FR": "MONTANT DEMANDÉ",
            "ES": "IMPORTE SOLICITADO",
            "GB": "REQUESTED AMOUNT"
        }
    },
    "request_ip": {
        "type": "keyword",
        "tags": ["IP"],
        "validations": ["ip"],
        "rules": ["blacklist"],
        "max_length": 15,
        "fake_type": "ip",
        "labels": {
            "IT": "IP DI PROVENIENZA DELLA RICHIESTA TELEMATICA",
            "DE": "QUELL-IP-ADRESSE DES ELEKTRONISCHEN ANTRAGS",
            "FR": "ADRESSE IP D’ORIGINE DE LA DEMANDE ÉLECTRONIQUE",
            "ES": "DIRECCIÓN IP DE ORIGEN DE LA SOLICITUD ELECTRÓNICA",
            "GB": "SOURCE IP ADDRESS OF THE ELECTRONIC REQUEST",
        }
    },
    "company_name": {
        "type": "string",
        "tags": ["Sheet", "COMPANY"],
        "list_view": True,
        "list_label": "COL_COMP_NAME",
        "required": True,
        "max_length": 100,
        "fake_type": "company_name",
        "labels": {
            "IT": "DENOMINAZIONE",
            "DE": "FIRMENBEZEICHNUNG",
            "FR": "DÉNOMINATION",
            "ES": "DENOMINACIÓN",
            "GB": "COMPANY NAME"
        }
    },
    "company_vat": {
        "type": "keyword",
        "tags": ["Sheet", "VAT"],
        "list_view": True,
        "list_label": "COL_COMP_VAT",
        "required": True,
        "validations": ["vat"],
        "rules": ["blacklist", "foreign_identifier"],
        "max_length": 30,
        "fake_type": "vat",
        "hint_key": "HINT_VAT",
        "labels": {
            "IT": "PARTITA IVA",
            "DE": "UST-IDNR.",      #"USt-IdNr.",
            "FR": "N° TVA",         #"N° TVA intracommunautaire",
            "ES": "NIF",
            "GB": "VAT REG. NO.",   #"VAT Registration No."
        }
    },
    "company_location": {
        "type": "string",
        "tags": ["Sheet", "LOCATION"],
        "max_length": 100,
        "fake_type": "location",
        "labels": {
            "IT": "SEDE LEGALE",
            "DE": "ORT DES FIRMENSITZES",
            "FR": "LOCALISATION DU SIÈGE SOCIAL",
            "ES": "LOCALIDAD DEL DOMICILIO SOCIAL",
            "GB": "REGISTERED OFFICE LOCATION",
        }
    },
    "company_iban": {
        "type": "keyword",
        "tags": ["IBAN"],
        "validations": ["iban"],
        "rules": ["blacklist", "foreign_identifier"],
        "max_length": 34,
        "fake_type": "iban",
        "hint_key": "HINT_IBAN",
        "labels": {
            "IT": "IBAN",
            "DE": "IBAN",
            "FR": "IBAN",
            "ES": "IBAN",
            "GB": "IBAN",
        }
    },
    "representative_fullname": {
        "type": "string",
        "tags": ["FULLNAME"],
        "rules": ["duplicate"],
        "max_length": 100,
        "fake_type": "profile",
        "sex_field": "representative_sex",
        "dob_field": "representative_dob",
        "tin_field": "representative_tin",
        "labels": {
            "IT": "NOME E COGNOME",
            "DE": "VORNAME UND NACHNAME",
            "FR": "PRÉNOM ET NOM",
            "ES": "NOMBRE Y APELLIDOS",
            "GB": "FIRST NAME AND LAST NAME",
        }
    },
    "representative_sex": {
        "type": "keyword",
        "max_length": 1,
        "fake_type": "profile",
        "hidden": True,
    },
    "representative_dob": {
        "type": "date",
        "max_length": 10,
        "fake_type": "profile",
        "hidden": True,
    },
    "representative_birthplace": {
        "type": "keyword",
        "max_length": 10,
        "fake_type": "profile",
        "hidden": True,
    },
    "representative_tin": {
        "type": "keyword",
        "tags": ["TIN"],
        "validations": ["tin"],
        "rules": ["blacklist", "duplicate", "tin_name_check", "foreign_identifier"],
        "max_length": 20,
        "fake_type": "profile",
        "hint_key": "HINT_TIN",
        "needs_tin_calc": True,
        "calc_fields": {
            "tin": "representative_tin",
            "fullname": "representative_fullname",
            "sex": "representative_sex",
            "dob": "representative_dob",
            "birthplace": "representative_birthplace"
        },
        "labels": {
            "IT": "CODICE FISCALE",
            "DE": "STEUER-ID",
            "FR": "NIR",
            "ES": "DNI",
            "GB": "NATIONAL INSURANCE NUMBER"
        }
    },
    "representative_email": {
        "type": "string",
        "tags": ["EMAIL"],
        "validations": ["email"],
        "max_length": 50,
        "fake_type": "email",
        "labels": {
            "IT": "INDIRIZZO PEC",
            "DE": "E-MAIL-ADRESSE",
            "FR": "ADRESSE E-MAIL",
            "ES": "DIRECCIÓN DE CORREO ELECTRÓNICO",
            "GB": "EMAIL ADDRESS"
        }
    },
    "representative_phone": {
        "type": "string",
        "tags": ["PHONE"],
        "validations": ["phone"],
        "max_length": 20,
        "fake_type": "phone",
        "labels": {
            "IT": "TELEFONO",
            "DE": "TELEFON",
            "FR": "TÉLÉPHONE",
            "ES": "TELÉFONO",
            "GB": "PHONE"
        }
    },
    "guarantor_1_fullname": {
        "type": "string",
        "tags": ["FULLNAME"],
        "rules": ["duplicate"],
        "max_length": 100,
        "fake_type": "profile",
        "sex_field": "guarantor_1_sex",
        "dob_field": "guarantor_1_dob",
        "tin_field": "guarantor_1_tin",
        "labels": {
            "IT": "NOME E COGNOME",
            "DE": "VORNAME UND NACHNAME",
            "FR": "PRÉNOM ET NOM",
            "ES": "NOMBRE Y APELLIDOS",
            "GB": "FIRST NAME AND LAST NAME"
        }
    },
    "guarantor_1_sex": {
        "type": "keyword",
        "max_length": 1,
        "fake_type": "profile",
        "hidden": True,
    },
    "guarantor_1_dob": {
        "type": "date",
        "max_length": 10,
        "fake_type": "profile",
        "hidden": True,
    },
    "guarantor_1_birthplace": {
        "type": "keyword",
        "max_length": 10,
        "fake_type": "profile",
        "hidden": True,
    },
    "guarantor_1_tin": {
        "type": "keyword",
        "tags": ["TIN"],
        "validations": ["tin"],
        "rules": ["blacklist", "duplicate", "tin_name_check", "foreign_identifier"],
        "max_length": 20,
        "fake_type": "profile",
        "hint_key": "HINT_TIN",
        "needs_tin_calc": True,
        "calc_fields": {
            "tin": "guarantor_1_tin",
            "fullname": "guarantor_1_fullname",
            "sex": "guarantor_1_sex",
            "dob": "guarantor_1_dob",
            "birthplace": "guarantor_1_birthplace"
        },
        "labels": {
            "IT": "CODICE FISCALE",
            "DE": "STEUER-ID",
            "FR": "NIR",
            "ES": "DNI",
            "GB": "NATIONAL INSURANCE NUMBER"
        }
    },
    "guarantor_2_fullname": {
        "type": "string",
        "tags": ["FULLNAME"],
        "rules": ["duplicate"],
        "max_length": 100,
        "fake_type": "profile",
        "sex_field": "guarantor_2_sex",
        "dob_field": "guarantor_2_dob",
        "tin_field": "guarantor_2_tin",
        "labels": {
            "IT": "NOME E COGNOME",
            "DE": "VORNAME UND NACHNAME",
            "FR": "PRÉNOM ET NOM",
            "ES": "NOMBRE Y APELLIDOS",
            "GB": "FIRST NAME AND LAST NAME"
        }
    },
    "guarantor_2_sex": {
        "type": "keyword",
        "max_length": 1,
        "fake_type": "profile",
        "hidden": True,
    },
    "guarantor_2_dob": {
        "type": "date",
        "max_length": 10,
        "fake_type": "profile",
        "hidden": True,
    },
    "guarantor_2_birthplace": {
        "type": "keyword",
        "max_length": 10,
        "fake_type": "profile",
        "hidden": True,
    },
    "guarantor_2_tin": {
        "type": "keyword",
        "tags": ["TIN"],
        "validations": ["tin"],
        "rules": ["blacklist", "duplicate", "tin_name_check", "foreign_identifier"],
        "max_length": 20,
        "fake_type": "profile",
        "hint_key": "HINT_TIN",
        "needs_tin_calc": True,
        "calc_fields": {
            "tin": "guarantor_2_tin",
            "fullname": "guarantor_2_fullname",
            "sex": "guarantor_2_sex",
            "dob": "guarantor_2_dob",
            "birthplace": "guarantor_2_birthplace"
        },
        "labels": {
            "IT": "CODICE FISCALE",
            "DE": "STEUER-ID",
            "FR": "NIR",
            "ES": "DNI",
            "GB": "NATIONAL INSURANCE NUMBER"
        }
    },
}

# Define the layout structure with localized Headers, Footer and Section
PDF = {
    "header": {
        "IT": "Domanda di Prestito",
        "DE": "Kreditantrag",
        "FR": "Demande de prêt",
        "ES": "Solicitud de préstamo",
        "GB": "Loan Application"
    },
    "footer": {
        "IT": "Scheda creata con dati sintetici a solo scopo di test",
        "DE": "Datenblatt mit synthetischen Daten ausschließlich zu Testzwecken erstellt",
        "FR": "Fiche créée à partir de données synthétiques à des fins de test uniquement",
        "ES": "Ficha creada con datos sintéticos exclusivamente para fines de prueba",
        "GB": "Sheet created using synthetic data for testing purposes only"
    }
}

SECTIONS = [
    {
        "internal_name": "request_data",
        "labels": {
            "IT": "DATI DELLA RICHIESTA",
            "DE": "ANTRAGSDATEN",
            "FR": "DONNÉES DE LA DEMANDE",
            "ES": "DATOS DE LA SOLICITUD",
            "GB": "APPLICATION DETAILS"
        },
        "fields": [
            "request_number",
            "request_branch_location",
            "request_amount",
            "request_ip",
        ]
    },
    {
        "internal_name": "company_profile",
        "labels": {
            "IT": "DATI DELL'AZIENDA",
            "DE": "UNTERNEHMENSDATEN",
            "FR": "DONNÉES DE L’ENTREPRISE",
            "ES": "DATOS DE LA EMPRESA",
            "GB": "COMPANY DETAILS"
        },
        "fields": [
            "company_name",
            "company_vat",
            "company_location",
            "company_iban",
        ]
    },
    {
        "internal_name": "legal_representative",
        "labels": {
            "IT": "DATI DEL LEGALE RAPPRESENTANTE",
            "DE": "DATEN DES GESETZLICHEN VERTRETERS",
            "FR": "DONNÉES DU REPRÉSENTANT LÉGAL",
            "ES": "DATOS DEL REPRESENTANTE LEGAL",
            "GB": "LEGAL REPRESENTATIVE DETAILS"
        },
        "fields": [
            "representative_fullname",
            "representative_sex",
            "representative_dob",
            "representative_birthplace",
            "representative_tin",
            "representative_email",
            "representative_phone"
        ]
    },
    {
        "internal_name": "guarantors",
        "labels": {
            "IT": "DATI DEI SOGGETTI GARANTI",
            "DE": "DATEN DER BÜRGEN",
            "FR": "DONNÉES DES GARANTS",
            "ES": "DATOS DE LOS GARANTES",
            "GB": "GUARANTORS DETAILS"
        },
        "fields": [
            "guarantor_1_fullname",
            "guarantor_1_sex",
            "guarantor_1_dob",
            "guarantor_1_birthplace",
            "guarantor_1_tin",
            "guarantor_2_fullname",
            "guarantor_2_sex",
            "guarantor_2_dob",
            "guarantor_2_birthplace",
            "guarantor_2_tin",
        ]
    }
]

def build_section_country_lookup():
    """
    Maps localized section headers to their country code.
    e.g., {"DATI DELLA RICHIESTA": "IT", "ANTRAGSDATEN": "DE", ...}
    """
    lookup = {}
    for section in SECTIONS:
        for lang, label in section.get("labels", {}).items():
            lookup[label] = lang.upper()
    return lookup

SECTION_COUNTRY_LOOKUP = build_section_country_lookup()

def _build_reverse_lookup_map():
    """
    Creates a dictionary like:
    {"PARTITA IVA": {"internal_name": "company_vat", "tags": ["Sheet", "VAT"], "validations": ["vat"], ...}, ...}
    for all languages.
    """
    lookup = {}
    for internal_name, config in FIELDS.items():
        for lang, label in config.get("labels", {}).items():
            # Clean label to match PDF extraction (trim spaces)
            clean_label = label.strip()
            lookup[clean_label] = {
                "internal_name": internal_name,
                "tags": config.get("tags", []),
                "validations": config.get("validations", []),
                "rules": config.get("rules", []),
                "required": config.get("required", False),
                "type": config.get("type", "string")
            }
    return lookup

REVERSE_LOOKUP = _build_reverse_lookup_map()


def _build_section_lookup():
    """Maps localized section headers (e.g., 'DATI DEI SOGGETTI GARANTI') -> 'guarantors'"""
    lookup = {}
    for section in SECTIONS:
        for lang, label in section.get("labels", {}).items():
            clean_label = label.strip()
            lookup[clean_label] = section["internal_name"]
    return lookup

# Maps "DATI DEI SOGGETTI GARANTI" -> "guarantors"
SECTION_LOOKUP = _build_section_lookup()

# Maps "guarantors" -> {"fields": ["guarantor_1_fullname", "guarantor_1_tin", ...]}
SECTIONS_BY_INTERNAL = {s["internal_name"]: s for s in SECTIONS}

def _build_section_by_field():
    """
    Reverse lookup: field_internal_name -> section dict.
    e.g. {'representative_tin': <legal_representative section dict>, ...}
    """
    lookup = {}
    for section in SECTIONS:
        for field_internal_name in section["fields"]:
            lookup[field_internal_name] = section
    return lookup

SECTION_BY_FIELD = _build_section_by_field()

def get_country_flag(country_code: str) -> str:
    """Converts a 2-letter country code (e.g., 'IT') into a Unicode Flag Emoji."""
    if not country_code or len(country_code) != 2:
        return ""

    # Regional Indicator Symbol logic (A=65, 🇦=0x1F1E6)
    offset = ord(country_code[0].upper()) - ord('A')
    flag = chr(0x1F1E6 + offset) + chr(0x1F1E6 + (ord(country_code[1].upper()) - ord('A')))
    return flag


def split_italian_full_name(full_name: str) -> tuple[str, str]:
    """
    Split a name using the convention: FIRST_NAME LAST_NAME.
    Supports common compound Italian surnames.
    """
    SURNAME_PARTICLES = {
        "DE", "DEL", "DEI", "DEGLI", "DELLA", "DELLE", "DI", "DA", "DAL",
        "DALLA", "DALL", "LA", "LE", "LO", "VAN", "VON",
    }

    parts = full_name.strip().split()

    if len(parts) < 2:
        raise ValueError("full_name must contain at least FIRST_NAME and LAST_NAME")

    surname_start = len(parts) - 1

    while surname_start > 0 and parts[surname_start - 1].upper() in SURNAME_PARTICLES:
        surname_start -= 1

    first_name = " ".join(parts[:surname_start])
    surname = " ".join(parts[surname_start:])

    if not first_name:
        raise ValueError(f"Could not determine first name from: {full_name!r}")

    return first_name, surname


