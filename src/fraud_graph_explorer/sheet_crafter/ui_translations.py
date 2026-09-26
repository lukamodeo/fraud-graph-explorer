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
        "it": "Profilo Paese da simulare:",
        "de": "Zu simulierendes Länderprofil:",
        "fr": "Profil Pays à simuler :",
        "es": "Perfil de País a simular:",
        "en-gb": "Country profile to simulate:"
        },
    "COUNTRY_HINT": {
        "it": "Aggiorna le regole sui formati VAT, TIN e IBAN da utilizzare, oltre che la lingua di compilazione.",
        "de": "Aktualisiert die anzuwendenden Formatregeln für VAT, TIN und IBAN sowie die Eingabesprache.",
        "fr": "Met à jour les règles de format VAT, TIN et IBAN à utiliser, ainsi que la langue de saisie.",
        "es": "Actualiza las reglas de formato de VAT, TIN e IBAN a utilizar, así como el idioma de introducción de datos.",
        "en-gb": "Updates the VAT, TIN, and IBAN format rules to apply, as well as the data-entry language."
        },
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
        # "de": "Geburtsdatum",
        "fr": "Date de Naissance",
        # "es": "Fecha de Nacimiento",
        # "en-gb": "Date of Birth"
    },
    "MODAL_SEX_LABEL": {
        "it": "Sesso",
        # "de": "Geschlecht",
        "fr": "Sexe",
        # "es": "Sexo",
        # "en-gb": "Sex"
    },
    "MODAL_SEX_MALE": {
        "it": "Maschio",
        # "de": "Männlich",
        "fr": "Masculin",
        # "es": "Masculino",
        # "en-gb": "Male"
    },
    "MODAL_SEX_FEMALE": {
        "it": "Femmina",
        # "de": "Weiblich",
        "fr": "Féminin",
        # "es": "Femenino",
        # "en-gb": "Female"
    },
    "MODAL_RECALC_TIN_LABEL": {
        "it": {
            "IT": "Ricalcola anche il Codice Fiscale.",
            # "DE": "Ricalcola anche lo Steuer-ID.",
            "FR": "Ricalcola anche il NIR.",
            # "ES": "Ricalcola anche il DNI.",
            # "GB": "Ricalcola anche il National Insurance number.",
        },
        "de": {
            "IT": "Auch den Codice Fiscale neu berechnen.",
            # "DE": "Auch die Steuer-ID neu berechnen.",
            "FR": "Auch die NIR neu berechnen.",
            # "ES": "Auch die DNI neu berechnen.",
            # "GB": "Auch die National Insurance number neu berechnen."
        },
        "fr": {
            "IT": "Recalculer également le Codice Fiscale.",
            # "DE": "Recalculer également la Steuer-ID.",
            "FR": "Recalculer également le NIR.",
            # "ES": "Recalculer également le DNI.",
            # "GB": "Recalculer également le National Insurance number."
        },
        "es": {
            "IT": "Recalcular también el Codice Fiscale.",
            # "DE": "Recalcular también la Steuer-ID.",
            "FR": "Recalcular también el NIR.",
            # "ES": "Recalcular también el DNI.",
            # "GB": "Recalcular también el National Insurance number."
        },
        "en-gb": {
            "IT": "Also recalculate the Codice Fiscale.",
            # "DE": "Also recalculate the Steuer-ID.",
            "FR": "Also recalculate the NIR.",
            # "ES": "Also recalculate the DNI.",
            # "GB": "Also recalculate the National Insurance number."
        }
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
            "IT": "La P.IVA italiana è un identificativo non derivato da dati dell'azienda.",
            "DE": "Lo USt-IdNr. tedesco è un identificativo non derivato da dati dell'azienda.",
            "FR": "La TVA francese è un identificativo non derivato da dati dell'azienda.",
            "ES": "Il NIF spagnolo è un identificativo non derivato da dati dell'azienda.",
            "GB": "La VAT britannica è un identificativo non derivato da dati dell'azienda.",
        },
        "de": {
            "IT": "Die italienische P.IVA ist eine Kennung, die nicht aus Unternehmensdaten abgeleitet wird.",
            "DE": "Die deutsche USt-IdNr. ist eine Kennung, die nicht aus Unternehmensdaten abgeleitet wird.",
            "FR": "Die französische TVA ist eine Kennung, die nicht aus Unternehmensdaten abgeleitet wird.",
            "ES": "Die spanische NIF ist eine Kennung, die nicht aus Unternehmensdaten abgeleitet wird.",
            "GB": "Die britische VAT ist eine Kennung, die nicht aus Unternehmensdaten abgeleitet wird."
        },
        "fr": {
            "IT": "La P.IVA italienne est un identifiant qui ne dérive pas des données de l’entreprise.",
            "DE": "La USt-IdNr. allemande est un identifiant qui ne dérive pas des données de l’entreprise.",
            "FR": "La TVA française est un identifiant qui ne dérive pas des données de l’entreprise.",
            "ES": "Le NIF espagnol est un identifiant qui ne dérive pas des données de l’entreprise.",
            "GB": "La VAT britannique est un identifiant qui ne dérive pas des données de l’entreprise."
        },
        "es": {
            "IT": "La P.IVA italiana es un identificador que no se deriva de los datos de la empresa.",
            "DE": "La USt-IdNr. alemana es un identificador que no se deriva de los datos de la empresa.",
            "FR": "La TVA francesa es un identificador que no se deriva de los datos de la empresa.",
            "ES": "El NIF español es un identificador que no se deriva de los datos de la empresa.",
            "GB": "La VAT británica es un identificador que no se deriva de los datos de la empresa."
        },
        "en-gb": {
            "IT": "The Italian P.IVA is an identifier not derived from company data.",
            "DE": "The German USt-IdNr. is an identifier not derived from company data.",
            "FR": "The French TVA is an identifier not derived from company data.",
            "ES": "The Spanish NIF is an identifier not derived from company data.",
            "GB": "The British VAT is an identifier not derived from company data."
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
    "HINT_RECALC": {
        "it": "Ricalcola",
        "de": "Neu berechnen",
        "fr": "Recalculer",
        "es": "Recalcular",
        "en-gb": "Recalculate"
    },
    "COUNTRY_NAMES": {
        "it": [('IT', '🇮🇹 Italia'), ('DE', '🇩🇪 Germania'), ('FR', '🇫🇷 Francia'), ('ES', '🇪🇸 Spagna'), ('GB', '🇬🇧 Regno Unito')],
        "de": [('IT', '🇮🇹 Italien'), ('DE', '🇩🇪 Deutschland'), ('FR', '🇫🇷 Frankreich'), ('ES', '🇪🇸 Spanien'), ('GB', '🇬🇧 Vereinigtes Königreich')],
        "fr": [('IT', '🇮🇹 Italie'), ('DE', '🇩🇪 Allemagne'), ('FR', '🇫🇷 France'), ('ES', '🇪🇸 Espagne'), ('GB', '🇬🇧 Royaume-Uni')],
        "es": [('IT', '🇮🇹 Italia'), ('DE', '🇩🇪 Alemania'), ('FR', '🇫🇷 Francia'), ('ES', '🇪🇸 España'), ('GB', '🇬🇧 Reino Unido')],
        "en-gb": [('IT', '🇮🇹 Italy'), ('DE', '🇩🇪 Germany'), ('FR', '🇫🇷 France'), ('ES', '🇪🇸 Spain'), ('GB', '🇬🇧 United Kingdom')]
    }
}

def get_ui_strings(lang_code: str, pdf_country_code: str = "GB") -> Dict[str, str]:
    lang = lang_code.lower()[:2]
    if lang == "en":
        lang = "en-gb"

    pdf_cc = pdf_country_code.upper()

    flat_dict = {}
    for key, val in UI_STRINGS.items():
        # Fallback just in case ever hardcoded a plain string
        if not isinstance(val, dict):
            flat_dict[key] = val
            continue

        # Safely check if this is a 2D structure by looking at the first value
        first_val = next(iter(val.values()), None)

        if isinstance(first_val, dict):
            # It's 2D: Get the context dictionary based on PDF country
            context_dict = val.get(lang, val.get("en-gb", {}))

            if isinstance(context_dict, dict):
                flat_dict[key] = context_dict.get(pdf_cc, context_dict.get("GB", ""))
            else:
                flat_dict[key] = ""
        else:
            # It's 1D: Get the string directly based on browser language
            flat_dict[key] = val.get(lang, val.get("en-gb", ""))

    return flat_dict

