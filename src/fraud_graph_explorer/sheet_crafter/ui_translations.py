# src/fraud_graph_explorer/sheet_crafter/ui_translations.py
from typing import Dict

# "Enum" keys mapped to localized strings
UI_STRINGS = {
    "TITLE": {
        "it": "Generatore di schede di prestito sintetiche",
        "de": "Generator für synthetische Kreditdatenblätter",
        "fr": "Générateur de fiches de prêt synthétiques",
        "es": "Generador de fichas de préstamo sintéticas",
        "en-gb": "Synthetic Loan Sheet Generator"
    },
    "HEADER": {
        "it": "Genera una scheda sintetica di richiesta di prestito",
        "de": "Ein synthetisches Kreditdatenblatt erstellen",
        "fr": "Générer une fiche de prêt synthétique",
        "es": "Generar una ficha de préstamo sintética",
        "en-gb": "Generate a Synthetic Loan Sheet"
    },
    "INSTRUCTIONS": {
        "it": "Seleziona un paese per auto-generare dati formalmente validi per quel paese.<br>Modifica i campi per iniettare anomalie nei dati.",
        "de": "Wählen Sie ein Land aus, um automatisch synthetische, für dieses Land formal gültige Daten zu generieren.<br>Bearbeiten Sie die Felder, um Anomalien in die Daten einzufügen.",
        "fr": "Sélectionnez un pays pour générer automatiquement des données synthétiques formellement valides pour ce pays.<br>Modifiez les champs pour introduire des anomalies dans les données.",
        "es": "Seleccione un país para generar automáticamente datos sintéticos formalmente válidos para ese país.<br>Modifique los campos para introducir anomalías en los datos.",
        "en-gb": "Select a country to automatically generate formally valid synthetic data for that country.<br>Edit the fields to inject anomalies into the data."
    },
    "COUNTRY_LABEL": {
        "it": "Paese",
        "de": "Land",
        "fr": "Pays",
        "es": "País",
        "en-gb": "Country"
    },
    "CHANGE_TO_AUTOGEN": {
        "it": "(cambia per auto-generare nuovi dati)",
        "de": "(ändern, um neue Daten zu generieren)",
        "fr": "(changer pour générer de nouvelles données)",
        "es": "(cambiar para autogenerar nuevos datos)",
        "en-gb": "(change to auto-generate new data)"
    },
    # "SECTION_REQUEST": {
    #     "it": "Dati Richiesta & Azienda",
    #     "de": "Antrags- & Unternehmensdaten",
    #     "fr": "Données de Demande & Entreprise",
    #     "es": "Datos de Solicitud & Empresa",
    #     "en-gb": "Request & Company Data"
    # },
    # "SECTION_LEGAL_REP": {
    #     "it": "Dati Rappresentante Legale",
    #     "de": "Daten des Gesetzlichen Vertreters",
    #     "fr": "Données du Représentant Légal",
    #     "es": "Datos del Representante Legal",
    #     "en-gb": "Legal Representative Data"
    # },
    # "HINT_VAT_RANDOM": {
    #     "it": "La P.IVA italiana è un codice non legato a dati personali.",
    #     "de": "USt-IdNr sind zufällig und nicht an personenbezogene Daten gebunden.",
    #     "fr": "Les TVA sont aléatoires et non liées à des données personnelles.",
    #     "es": "Los NIF son aleatorios y no vinculados a datos personales.",
    #     "en-gb": "Company VATs are random and not tied to personal data."
    # },
    # "HINT_VAT_IT": {
    #     "it": "La P.IVA italiana è un identificativo non legato a dati personali.",
    #     "de": "Die italienische P.IVA ist eine Kennung, die nicht mit personenbezogenen Daten verknüpft ist.",
    #     "fr": "La P.IVA italienne est un identifiant non lié à des données personnelles.",
    #     "es": "El P.IVA italiano es un identificador que no está vinculado a datos personales.",
    #     "en-gb": "The Italian P.IVA is an identifier not linked to personal data."
    # },
    # "HINT_VAT_DE": {
    #     "it": "La USt-IdNr. tedesca è un identificativo non legato a dati personali.",
    #     "de": "Die deutsche USt-IdNr. ist eine Kennung, die nicht mit personenbezogenen Daten verknüpft ist.",
    #     "fr": "La USt-IdNr. allemande est un identifiant non lié à des données personnelles.",
    #     "es": "El USt-IdNr. alemán es un identificador que no está vinculado a datos personales.",
    #     "en-gb": "The German USt-IdNr. is an identifier not linked to personal data."
    # },
    # "HINT_VAT_FR": {
    #     "it": "La TVA francese è un identificativo non legato a dati personali.",
    #     "de": "Die französische TVA ist eine Kennung, die nicht mit personenbezogenen Daten verknüpft ist.",
    #     "fr": "La TVA française est un identifiant non lié à des données personnelles.",
    #     "es": "El TVA francés es un identificador que no está vinculado a datos personales.",
    #     "en-gb": "The French TVA is an identifier not linked to personal data."
    # },
    # "HINT_VAT_ES": {
    #     "it": "Il NIF spagnolo è un identificativo non legato a dati personali.",
    #     "de": "Die spanische NIF ist eine Kennung, die nicht mit personenbezogenen Daten verknüpft ist.",
    #     "fr": "Le NIF espagnol est un identifiant non lié à des données personnelles.",
    #     "es": "El NIF español es un identificador que no está vinculado a datos personales.",
    #     "en-gb": "The Spanish NIF is an identifier not linked to personal data."
    # },
    # "HINT_VAT_GB": {
    #     "it": "La VAT britannica è un identificativo non legato a dati personali.",
    #     "de": "Die britische VAT-Nummer ist eine Kennung, die nicht mit personenbezogenen Daten verknüpft ist.",
    #     "fr": "La VAT britannique est un identifiant non lié à des données personnelles.",
    #     "es": "El VAT británico es un identificador que no está vinculado a datos personales.",
    #     "en-gb": "The UK VAT number is an identifier not linked to personal data."
    # },
    # "HINT_TIN": {
    #     "it": "I Codici Fiscali italiani sono legati anche a Nome/Cognome e Sesso. Modificando uno di essi, il CF diventa non valido.",
    #     "de": "Italienische TINs sind an Name und Geburtsdatum gebunden. Bei Namensänderung wird die TIN ungültig.",
    #     "fr": "Les TIN italiens sont liés au nom et à la date de naissance. Changer le nom invalide le TIN.",
    #     "es": "Los TIN italianos están vinculados al nombre y fecha de nacimiento. Cambiar el nombre invalida el TIN.",
    #     "en-gb": "Italian TINs are algorithmically tied to Name and DOB. If you change the name, this TIN becomes invalid."
    # },
    # "HINT_TIN_IT": {
    #     "it": "Il Codice Fiscale italiano è legato a Nome, Cognome, Sesso e Data di Nascita. Modificando uno di essi, il C.F. risulta non più valido.",
    #     "de": "Italienische Steuernummern (TIN) sind an Name, Geburtsdatum und Geschlecht gebunden.<br>Bei Änderung wird die TIN ungültig.",
    #     "fr": "Les codes fiscaux italiens sont liés au nom, à la date de naissance et au sexe.<br>Les modifier invalide le code.",
    #     "es": "Los códigos fiscales italianos están vinculados al nombre, fecha de nacimiento y sexo.<br>Cambiarlos invalida el código.",
    #     "en-gb": "Italian TINs are algorithmically tied to Name, DOB, and Sex.<br>If you change any of them, the TIN becomes invalid."
    # },
    # "HINT_TIN_FR": {
    #     "it": "Il NIR francese è legato a Sesso e Data di Nascita.<br>Modificando uno di essi, il NIR risulta non più valido.",
    #     "de": "Französische NIR sind an Geschlecht und Geburtsdatum gebunden.<br>Bei Änderung wird der NIR ungültig.",
    #     "fr": "Les NIR français sont liés au sexe et à la date de naissance.<br>Les modifier invalide le NIR.",
    #     "es": "Los NIR franceses están vinculados al sexo y fecha de nacimiento.<br>Cambiarlos invalida el NIR.",
    #     "en-gb": "French NIRs are tied to Sex and DOB.<br>If you change them, the NIR becomes invalid."
    # },
    # "HINT_TIN_RANDOM": {
    #     "it": "I TIN sono numeri casuali e non legati a dati personali.",
    #     "de": "TINs sind zufällige Verwaltungsnummern und nicht an personenbezogene Daten gebunden.",
    #     "fr": "Les TIN sont des numéros aléatoires et non liés à des données personnelles.",
    #     "es": "Los TIN son números administrativos aleatorios y no vinculados a datos personales.",
    #     "en-gb": "TINs are random administrative numbers and are not tied to personal data."
    # },
    "BTN_RANDOMIZE": {
        "it": "Genera Nuovi Dati",
        "de": "Neue Daten Generieren",
        "fr": "Générer Nouvelles Données",
        "es": "Generar Nuevos Datos",
        "en-gb": "Re-fetch Fake Data"
    },
    "BTN_SAVE": {
        "it": "Salva come PDF",
        "de": "Als PDF speichern",
        "fr": "Enregistrer au format PDF",
        "es": "Guardar como PDF",
        "en-gb": "Save as PDF"
    },
    "PDF_DATA": {
        "it": "Compilazione e anteprima dati PDF",
        "de": "Eingabe und Vorschau der PDF-Daten",
        "fr": "Saisie et aperçu des données du PDF",
        "es": "Introducción y vista previa de los datos del PDF",
        "en-gb": "PDF data entry and preview"
    },
    "MODAL_TITLE": {
        "it": "Aggiornamento dati anagrafici",
        "de": "Aktualisierung der persönlichen Daten",
        "fr": "Mise à jour des données personnelles",
        "es": "Actualización de los datos personales",
        "en-gb": "Personal details update"
    },
    "MODAL_INSTRUCTIONS": {
        "it": "A seguito della modifica di Nome e Cognome,<br>puoi confermare o aggiornare anche i seguenti dati:",
        "de": "Nach einer Änderung von Vorname und Nachname<br>können Sie auch die folgenden Daten bestätigen oder aktualisieren",
        "fr": "À la suite de la modification du prénom et du nom,<br>vous pouvez également confirmer ou mettre à jour les données suivantes",
        "es": "Tras modificar el nombre y los apellidos,<br>también puede confirmar o actualizar los siguientes datos",
        "en-gb": "Following a change to First Name and Last Name,<br>you can also confirm or update the following details"
    },
    "MODAL_DOB_LABEL": {
        "it": "Data di Nascita",
        "de": "Geburtsdatum",
        "fr": "Date de Naissance",
        "es": "Fecha de Nacimiento",
        "en-gb": "Date of Birth"
    },
    "MODAL_SEX_LABEL": {
        "it": "Sesso",
        "de": "Geschlecht",
        "fr": "Sexe",
        "es": "Sexo",
        "en-gb": "Sex"
    },
    "MODAL_SEX_PLACEHOLDER": {
        "it": "-- Seleziona --",
        "de": "-- Auswählen --",
        "fr": "-- Sélectionner --",
        "es": "-- Seleccionar --",
        "en-gb": "-- Select --"
    },
    "MODAL_SEX_MALE": {
        "it": "Maschio",
        "de": "Männlich",
        "fr": "Masculin",
        "es": "Masculino",
        "en-gb": "Male"
    },
    "MODAL_SEX_FEMALE": {
        "it": "Femmina",
        "de": "Weiblich",
        "fr": "Féminin",
        "es": "Femenino",
        "en-gb": "Female"
    },
    "MODAL_BTN": {
        "it": "Salva",
        "de": "Speichern",
        "fr": "Enregistrer",
        "es": "Guardar",
        "en-gb": "Save"
    },
    "HINT_VAT": {
        "it": {
            "IT": "La P.IVA italiana è un identificativo non derivato da dati personali.",
            "DE": "Lo USt-IdNr. tedesco è un identificativo non derivato da dati personali.",
            "FR": "La TVA francese è un identificativo non derivato da dati personali.",
            "ES": "Il NIF spagnolo è un identificativo non derivato da dati personali.",
            "GB": "La VAT britannica è un identificativo non derivato da dati personali.",
        },
        "de": {
            "IT": "Die italienische P.IVA ist eine Kennung, die nicht aus personenbezogenen Daten.",
            "DE": "Die deutsche USt-IdNr. ist eine Kennung, die nicht aus personenbezogenen Daten.",
            "FR": "Die französische TVA ist eine Kennung, die nicht aus personenbezogenen Daten.",
            "ES": "Die spanische NIF ist eine Kennung, die nicht aus personenbezogenen Daten.",
            "GB": "Die britische VAT-Nummer ist eine Kennung, die nicht aus personenbezogenen Daten.",
        },
        "fr": {
            "IT": "La P.IVA italienne est un identifiant qui ne dérive pas de données personnelles.",
            "DE": "La USt-IdNr. allemande est un identifiant qui ne dérive pas de données personnelles.",
            "FR": "La TVA française est un identifiant qui ne dérive pas de données personnelles.",
            "ES": "Le NIF espagnol est un identifiant qui ne dérive pas de données personnelles.",
            "GB": "La VAT britannique est un identifiant qui ne dérive pas de données personnelles.",
        },
        "es": {
            "IT": "El P.IVA italiano es un identificador que no se deriva de datos personales.",
            "DE": "El USt-IdNr. alemán es un identificador que no se deriva de datos personales.",
            "FR": "El TVA francés es un identificador que no se deriva de datos personales.",
            "ES": "El NIF español es un identificador que no se deriva de datos personales.",
            "GB": "El VAT británico es un identificador que no se deriva de datos personales.",
        },
        "en-gb": {
            "IT": "The Italian P.IVA is an identifier not derived from personal data.",
            "DE": "The German USt-IdNr. is an identifier not derived from personal data.",
            "FR": "The French TVA is an identifier not derived from personal data.",
            "ES": "The Spanish NIF is an identifier not derived from personal data.",
            "GB": "The UK VAT number is an identifier not derived from personal data.",
        },
    },
    "HINT_TIN": {
        "it": {
            "IT": "Il Codice Fiscale italiano è un identificativo derivato da Nome, Cognome, Sesso e Data di Nascita. Modificando uno di essi, il C.F. risulta non più valido.",
            "DE": "Lo Steuer-ID tedesco è un identificativo non derivato da dati personali quali Nome, Cognome, Sesso o Data di Nascita.",
            "FR": "Il NIR francese è un identificativo derivato da Sesso e Data di Nascita. Modificando uno di essi, il NIR risulta non più valido.",
            "ES": "Il DNI spagnolo è un identificativo non derivato da dati personali quali Nome, Cognome, Sesso o Data di Nascita.",
            "GB": "Il National Insurance number britannico è un identificativo non derivato da dati personali quali Nome, Cognome, Sesso o Data di Nascita.",
        },
        "de": {
            "IT": "Der italienische Codice Fiscale ist eine Kennung, die aus Vorname, Nachname, Geschlecht und Geburtsdatum abgeleitet wird. Wird eines dieser Merkmale geändert, ist der C.F. nicht mehr gültig.",
            "DE": "Die deutsche Steuer-ID ist eine Kennung, die nicht aus personenbezogenen Daten wie Vorname, Nachname, Geschlecht oder Geburtsdatum abgeleitet wird.",
            "FR": "Die französische NIR ist eine Kennung, die aus Geschlecht und Geburtsdatum abgeleitet wird. Wird eines dieser Merkmale geändert, ist die NIR nicht mehr gültig.",
            "ES": "Die spanische DNI ist eine Kennung, die nicht aus personenbezogenen Daten wie Vorname, Nachname, Geschlecht oder Geburtsdatum abgeleitet wird.",
            "GB": "Die britische National Insurance number ist eine Kennung, die nicht aus personenbezogenen Daten wie Vorname, Nachname, Geschlecht oder Geburtsdatum abgeleitet wird."
        },
        "fr": {
            "IT": "Le Codice Fiscale italien est un identifiant dérivé du prénom, du nom, du sexe et de la date de naissance. Si l’un de ces éléments est modifié, le C.F. n’est plus valide.",
            "DE": "La Steuer-ID allemande est un identifiant qui ne dérive pas de données personnelles telles que le prénom, le nom, le sexe ou la date de naissance.",
            "FR": "Le NIR français est un identifiant dérivé du sexe et de la date de naissance. Si l’un de ces éléments est modifié, le NIR n’est plus valide.",
            "ES": "Le DNI espagnol est un identifiant qui ne dérive pas de données personnelles telles que le prénom, le nom, le sexe ou la date de naissance.",
            "GB": "Le National Insurance number britannique est un identifiant qui ne dérive pas de données personnelles telles que le prénom, le nom, le sexe ou la date de naissance."
        },
        "es": {
            "IT": "El Codice Fiscale italiano es un identificador derivado del nombre, los apellidos, el sexo y la fecha de nacimiento. Si se modifica alguno de estos datos, el C.F. deja de ser válido.",
            "DE": "La Steuer-ID alemana es un identificador que no se deriva de datos personales como el nombre, los apellidos, el sexo o la fecha de nacimiento.",
            "FR": "El NIR francés es un identificador derivado del sexo y la fecha de nacimiento. Si se modifica alguno de estos datos, el NIR deja de ser válido.",
            "ES": "El DNI español es un identificador que no se deriva de datos personales como el nombre, los apellidos, el sexo o la fecha de nacimiento.",
            "GB": "El National Insurance number británico es un identificador que no se deriva de datos personales como el nombre, los apellidos, el sexo o la fecha de nacimiento."
        },
        "en-gb": {
            "IT": "The Italian Codice Fiscale is an identifier derived from First Name, Last Name, Sex and Date of Birth. If any of these are changed, the C.F. is no longer valid.",
            "DE": "The German Steuer-ID is an identifier not derived from personal data such as First Name, Last Name, Sex or Date of Birth.",
            "FR": "The French NIR is an identifier derived from Sex and Date of Birth. If either of these is changed, the NIR is no longer valid.",
            "ES": "The Spanish DNI is an identifier not derived from personal data such as First Name, Last Name, Sex or Date of Birth.",
            "GB": "The UK National Insurance number is an identifier not derived from personal data such as First Name, Last Name, Sex or Date of Birth."
        }
    },
    "COUNTRY_NAMES": {
        "it": [('IT', 'Italia'), ('DE', 'Germania'), ('FR', 'Francia'), ('ES', 'Spagna'), ('GB', 'Regno Unito')],
        "de": [('IT', 'Italien'), ('DE', 'Deutschland'), ('FR', 'Frankreich'), ('ES', 'Spanien'), ('GB', 'Vereinigtes Königreich')],
        "fr": [('IT', 'Italie'), ('DE', 'Allemagne'), ('FR', 'France'), ('ES', 'Espagne'), ('GB', 'Royaume-Uni')],
        "es": [('IT', 'Italia'), ('DE', 'Alemania'), ('FR', 'Francia'), ('ES', 'España'), ('GB', 'Reino Unido')],
        "en-gb": [('IT', 'Italy'), ('DE', 'Germany'), ('FR', 'France'), ('ES', 'Spain'), ('GB', 'United Kingdom')]
    }
}


# def get_ui_strings(lang_code: str) -> dict:
#     """Returns a flat dictionary of strings for the given language."""
#     # Normalize language code (e.g., 'en-us' -> 'en-gb', 'it' -> 'it')
#     lang = lang_code.lower()[:2]
#     if lang == "en":
#         lang = "en-gb"
#
#     # Fallback to en-gb if language not found
#     return {key: val.get(lang, val["en-gb"]) for key, val in UI_STRINGS.items()}

def get_ui_strings(lang_code: str, pdf_country_code: str = "GB") -> Dict[str, str]:
    lang = lang_code.lower()[:2]
    if lang == "en":
        lang = "en-gb"

    pdf_cc = pdf_country_code.upper()

    print(f"{lang_code} - {pdf_cc}")

    flat_dict = {}
    for key, val in UI_STRINGS.items():
        # Fallback just in case ever hardcoded a plain string
        if not isinstance(val, dict):
            print(f"01 - {key}")
            flat_dict[key] = val
            continue

        # Safely check if this is a 2D structure by looking at the first value
        first_val = next(iter(val.values()), None)

        if isinstance(first_val, dict):
            print(f"02 - {key}")
            # It's 2D: Get the context dictionary based on PDF country
            context_dict = val.get(lang, val.get("en-gb", {}))

            # PyCharm is happy because we explicitly check the type
            if isinstance(context_dict, dict):
                print(f"02a - {key}")
                flat_dict[key] = context_dict.get(pdf_cc, context_dict.get("GB", ""))
            else:
                print(f"02b - {key}")
                flat_dict[key] = ""
        else:
            print(f"03 - {key}")
            # It's 1D: Get the string directly based on browser language
            flat_dict[key] = val.get(lang, val.get("en-gb", ""))

    return flat_dict


# if __name__ == "__main__":
#     print("OK")
#     ui_strings = get_ui_strings("it-IT", "DE")
#     print("*" * 100)
#     print(ui_strings["HEADER"])
#     print("*" * 100)
#     print(ui_strings["HINT_TIN"])
#     print("*" * 100)
