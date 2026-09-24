# src/fraud_graph_explorer/graph_explorer/ingestion_schema.py

# Define the business logic (language-agnostic)
FIELDS = {
    "request_number": {
        "type": "string",
        "tags": ["Sheet"],
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
    "company_name": {
        "type": "string",
        "tags": ["Sheet", "COMPANY"],
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
        "type": "string",
        "tags": ["Sheet", "VAT"],
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
        "type": "string",
        "tags": ["IBAN"],
        "max_length": 34,
        "fake_type": "iban",
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
        "type": "string",
        "tags": [],
        "max_length": 1,
        "fake_type": "profile",
        "hidden": True,
    },
    "representative_dob": {
        "type": "string",
        "tags": [],
        "max_length": 10,
        "fake_type": "profile",
        "hidden": True,
    },
    "representative_birthplace": {
        "type": "string",
        "tags": [],
        "max_length": 10,
        "fake_type": "profile",
        "hidden": True,
    },
    "representative_tin": {
        "type": "keyword",
        "tags": ["TIN"],
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
        "tags": ["email"],
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
        "type": "string",
        "tags": [],
        "max_length": 1,
        "fake_type": "profile",
        "hidden": True,
    },
    "guarantor_1_dob": {
        "type": "string",
        "tags": [],
        "max_length": 10,
        "fake_type": "profile",
        "hidden": True,
    },
    "guarantor_1_birthplace": {
        "type": "string",
        "tags": [],
        "max_length": 10,
        "fake_type": "profile",
        "hidden": True,
    },
    "guarantor_1_tin": {
        "type": "keyword",
        "tags": ["TIN"],
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
        "type": "string",
        "tags": [],
        "max_length": 1,
        "fake_type": "profile",
        "hidden": True,
    },
    "guarantor_2_dob": {
        "type": "string",
        "tags": [],
        "max_length": 10,
        "fake_type": "profile",
        "hidden": True,
    },
    "guarantor_2_birthplace": {
        "type": "string",
        "tags": [],
        "max_length": 10,
        "fake_type": "profile",
        "hidden": True,
    },
    "guarantor_2_tin": {
        "type": "keyword",
        "tags": ["TIN"],
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
            "company_iban"
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