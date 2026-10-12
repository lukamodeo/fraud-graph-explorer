# src/fraud_graph_explorer/graph_explorer/ui_translations.py
from typing import Dict

UI_STRINGS = {
    "COUNTRY_NAMES": {
        "it": [('IT', '🇮🇹 Italia'), ('DE', '🇩🇪 Germania'), ('FR', '🇫🇷 Francia'), ('ES', '🇪🇸 Spagna'), ('GB', '🇬🇧 Regno Unito')],
        "de": [('IT', '🇮🇹 Italien'), ('DE', '🇩🇪 Deutschland'), ('FR', '🇫🇷 Frankreich'), ('ES', '🇪🇸 Spanien'), ('GB', '🇬🇧 Vereinigtes Königreich')],
        "fr": [('IT', '🇮🇹 Italie'), ('DE', '🇩🇪 Allemagne'), ('FR', '🇫🇷 France'), ('ES', '🇪🇸 Espagne'), ('GB', '🇬🇧 Royaume-Uni')],
        "es": [('IT', '🇮🇹 Italia'), ('DE', '🇩🇪 Alemania'), ('FR', '🇫🇷 Francia'), ('ES', '🇪🇸 España'), ('GB', '🇬🇧 Reino Unido')],
        "en-gb": [('IT', '🇮🇹 Italy'), ('DE', '🇩🇪 Germany'), ('FR', '🇫🇷 France'), ('ES', '🇪🇸 Spain'), ('GB', '🇬🇧 United Kingdom')]
    },
    "TAB_01": {
        "it": "Gestione domande",
        "de": "Antragsverwaltung",
        "fr": "Gestion des demandes",
        "es": "Gestión solicitudes",
        "en-gb": "Application Management"
        },
    "TAB_02": {
        "it": "Esplorazione grafo",
        "de": "Graph erkunden",
        "fr": "Exploration du graphe",
        "es": "Exploración grafo",
        "en-gb": "Graph Explorer"
        },
    "TAB_03": {
        "it": "Confronto domande",
        "de": "Antragsvergleich",
        "fr": "Comparaison des demandes",
        "es": "Comparación solicitudes",
        "en-gb": "Application Comparison"
        },
    "TAB_04": {
        "it": "Informazioni",
        "de": "Info",
        "fr": "À propos",
        "es": "Acerca de",
        "en-gb": "About"
        },
    "UPLOAD_TITLE": {
        "it": "Nuova Domanda di Prestito",
        "de": "Neuer Kreditantrag",
        "fr": "Nouvelle demande de prêt",
        "es": "Nueva solicitud de préstamo",
        "en-gb": "New Loan Application"
        },
    "UPLOAD_LABEL": {
        "it": "Seleziona un file PDF",
        "de": "Wählen Sie eine PDF-Datei",
        "fr": "Sélectionner un fichier PDF",
        "es": "Seleccione un archivo PDF",
        "en-gb": "Select a PDF file"
        },
    "UPLOAD_BTN_SUBMIT": {
        "it": "Carica e processa",
        "de": "Hochladen und Verarbeiten",
        "fr": "Charger et Traiter",
        "es": "Cargar y Procesar",
        "en-gb": "Load and Process"
        },
    "LIST_TITLE": {
        "it": "Domande di Prestito",
        "de": "Kreditanträge",
        "fr": "Demandes de prêt",
        "es": "Solicitudes de préstamo",
        "en-gb": "Loan Applications"
        },
    "FILTER_TITLE": {
        "it": "Filtri di Ricerca",
        "de": "Suchfilter",
        "fr": "Filtres de recherche",
        "es": "Filtros de búsqueda",
        "en-gb": "Search Filters"
        },
    "FILTERS_APPLIED": {
        "it": "Filtri applicati",
        "de": "Angewandte Filter",
        "fr": "Filtres appliqués",
        "es": "Filtros aplicados",
        "en-gb": "Applied filters"
        },
    "FILTER_SEARCH": {
        "it": "Cerca in tutto il testo",
        "de": "Im gesamten Text suchen",
        "fr": "Rechercher dans tout le texte",
        "es": "Buscar en todo el texto",
        "en-gb": "Search all text"
        },
    "FILTER_PLACEHOLDER": {
        "it": "es. Mario*, IT123*",
        "de": "z.B. Mario*, IT123*",
        "fr": "ex. Mario*, IT123*",
        "es": "ej. Mario*, IT123*",
        "en-gb": "e.g., Mario*, IT123*"
        },
    "FILTER_COUNTRY": {
        "it": "Paese",
        "de": "Land",
        "fr": "Pays",
        "es": "País",
        "en-gb": "Country"
        },
    "FILTER_ALL": {
        "it": "Tutti",
        "de": "Alle",
        "fr": "Tous",
        "es": "Todos",
        "en-gb": "All"
        },
    "FILTER_STATUS": {
        "it": "Stato",
        "de": "Status",
        "fr": "Statut",
        "es": "Estado",
        "en-gb": "Status"
        },
    "FILTER_STATUS_OK": {
        "it": "Ok",
        "de": "Ok",
        "fr": "Ok",
        "es": "Ok",
        "en-gb": "OK"
        },
    "FILTER_STATUS_ERR": {
        "it": "Con errori",
        "de": "Mit Fehlern",
        "fr": "Avec erreurs",
        "es": "Con errores",
        "en-gb": "With errors"
        },
    "FILTER_STATUS_WARN": {
        "it": "Con avvisi",
        "de": "Mit Warnungen",
        "fr": "Avec avertissements",
        "es": "Con advertencias",
        "en-gb": "With warnings"
        },
    "FILTER_STATUS_ERR_OR_WARN": {
        "it": "Con errori o avvisi",
        "de": "Mit Fehlern oder Warnungen",
        "fr": "Avec erreurs ou avertissements",
        "es": "Con errores o advertencias",
        "en-gb": "With errors or warnings"
        },
    "FILTER_START_DATE": {
        "it": "Dal",
        "de": "Von",
        "fr": "De",
        "es": "Desde",
        "en-gb": "From"
        },
    "FILTER_END_DATE": {
        "it": "Al",
        "de": "Bis",
        "fr": "À",
        "es": "Hasta",
        "en-gb": "To"
        },
    "FILTER_BTN_CLEAR": {
        "it": "Rimuovi Filtri",
        "de": "Filter löschen",
        "fr": "Effacer les filtres",
        "es": "Borrar filtros",
        "en-gb": "Clear Filters"
        },
    "CARD_VAL_ERRORS": {
        "it": "Errori di validazione",
        "de": "Validierungsfehler",
        "fr": "Erreurs de validation",
        "es": "Errores de validación",
        "en-gb": "Validation errors"
        },
    "CARD_RULE_WARNINGS": {
        "it": "Avvisi",
        "de": "Warnungen",
        "fr": "Avertissements",
        "es": "Advertencias",
        "en-gb": "Warnings"
    },
    "CARD_NO_ERR": {
        "it": "Nessun errore di validazione",
        "de": "Keine Validierungsfehler",
        "fr": "Aucune erreur de validation",
        "es": "Sin errores de validación",
        "en-gb": "No validation errors"
        },
    "CARD_NO_WARN": {
        "it": "Nessun avviso",
        "de": "Keine Warnungen",
        "fr": "Aucun avertissement",
        "es": "Sin advertencias",
        "en-gb": "No warnings"
        },
    "CARD_NO_DATA": {
        "it": "Nessuna Domanda di Prestito selezionata",
        "de": "Kein Kreditantrag ausgewählt",
        "fr": "Aucune demande de prêt sélectionnée",
        "es": "No se ha seleccionado ninguna solicitud de préstamo",
        "en-gb": "No loan application selected"
        },
    "CARD_SELECTED": {
        "it": "Selezionato: {req_num}",
        "de": "Ausgewählt: {req_num}",
        "fr": "Sélectionné : {req_num}",
        "es": "Seleccionado: {req_num}",
        "en-gb": "Selected: {req_num}"
        },
    "PAG_PAGE_OF": {
        "it": "Pagina {current} di {total}",
        "de": "Seite {current} von {total}",
        "fr": "Page {current} sur {total}",
        "es": "Página {current} de {total}",
        "en-gb": "Page {current} of {total}"
    },
    "PAG_FIRST": {
        "it": "Prima",
        "de": "Erste",
        "fr": "Première",
        "es": "Primera",
        "en-gb": "First"
    },
    "PAG_PREV": {
        "it": "Precedente",
        "de": "Zurück",
        "fr": "Précédent",
        "es": "Anterior",
        "en-gb": "Previous"
    },
    "PAG_NEXT": {
        "it": "Successiva",
        "de": "Weiter",
        "fr": "Suivant",
        "es": "Siguiente",
        "en-gb": "Next"
    },
    "PAG_LAST": {
        "it": "Ultima",
        "de": "Letzte",
        "fr": "Dernière",
        "es": "Última",
        "en-gb": "Last"
    },
    "DEL_TITLE": {
        "it": "Conferma Eliminazione",
        "de": "Löschen bestätigen",
        "fr": "Confirmer la suppression",
        "es": "Confirmar eliminación",
        "en-gb": "Confirm Deletion"
    },
    "DEL_MSG": {
        "it": "Sei sicuro di voler eliminare la domanda <b id='del-req-num'></b>?<br>Questa azione è irreversibile.",
        "de": "Möchten Sie den Antrag <b id='del-req-num'></b> wirklich löschen?<br>Diese Aktion ist unwiderruflich.",
        "fr": "Êtes-vous sûr de vouloir supprimer la demande <b id='del-req-num'></b> ?<br>Cette action est irréversible.",
        "es": "¿Está seguro de que desea eliminar la solicitud <b id='del-req-num'></b>?<br>Esta acción es irreversible.",
        "en-gb": "Are you sure you want to delete application <b id='del-req-num'></b>?<br>This action is irreversible."
    },
    "DEL_BTN_CONFIRM": {
        "it": "Elimina",
        "de": "Löschen",
        "fr": "Supprimer",
        "es": "Eliminar",
        "en-gb": "Delete"
    },
    "DEL_BTN_CANCEL": {
        "it": "Annulla",
        "de": "Abbrechen",
        "fr": "Annuler",
        "es": "Cancelar",
        "en-gb": "Cancel"
    },
    "DUP_TITLE": {
        "it": "Duplicato Rilevato",
        "de": "Duplikat erkannt",
        "fr": "Doublon détecté",
        "es": "Duplicado detectado",
        "en-gb": "Duplicate Detected"
    },
    "DUP_MSG": {
        "it": "La domanda <b>{req_num}</b> esiste già (File: <i>{old_file}</i>).<br>Vuoi sovrascrivere il record e il file?",
        "de": "Antrag <b>{req_num}</b> existiert bereits (Datei: <i>{old_file}</i>).<br>Möchten Sie den Datensatz und die Datei überschreiben?",
        "fr": "La demande <b>{req_num}</b> existe déjà (Fichier : <i>{old_file}</i>).<br>Voulez-vous écraser l'enregistrement et le fichier ?",
        "es": "La solicitud <b>{req_num}</b> ya existe (Archivo: <i>{old_file}</i>).<br>¿Desea sobrescribir el registro y el archivo?",
        "en-gb": "Application <b>{req_num}</b> already exists (File: <i>{old_file}</i>).<br>Do you want to overwrite the record and file?"
    },
    "DUP_BTN_OVERWRITE": {
        "it": "Sovrascrivi",
        "de": "Überschreiben",
        "fr": "Écraser",
        "es": "Sobrescribir",
        "en-gb": "Overwrite"
    },
    "DUP_BTN_CANCEL": {
        "it": "Annulla",
        "de": "Abbrechen",
        "fr": "Annuler",
        "es": "Cancelar",
        "en-gb": "Cancel"
    },
    "INGEST_SUCCESS": {
        "it": "Inserito: {req_num}",
        "de": "Erfasst: {req_num}",
        "fr": "Intégré : {req_num}",
        "es": "Ingestado: {req_num}",
        "en-gb": "Ingested: {req_num}"
        },
    "INGEST_OVERWRITTEN": {
        "it": "Sovrascritto: {req_num}",
        "de": "Überschrieben: {req_num}",
        "fr": "Écrasé : {req_num}",
        "es": "Sobrescrito: {req_num}",
        "en-gb": "Overwritten: {req_num}"
        },
    "INGEST_CANCELLED": {
        "it": "Operazione annullata.",
        "de": "Vorgang abgebrochen.",
        "fr": "Opération annulée.",
        "es": "Operación cancelada.",
        "en-gb": "Operation Cancelled."
        },
    "INGEST_ERR_DUPLICATE": {
        "it": "Saltato: {req_num} già inserito.",
        "de": "Übersprungen: {req_num} bereits erfasst.",
        "fr": "Ignoré : {req_num} déjà intégré.",
        "es": "Omitido: {req_num} ya ingestado.",
        "en-gb": "Skipped: {req_num} already ingested."
    },
    "INGEST_ERR_INVALID_SHEET": {
        "it": "Fallito: Il PDF non contiene una Domanda di Prestito valida.",
        "de": "Fehlgeschlagen: PDF enthält keinen gültigen Kreditantrag.",
        "fr": "Échec : Le PDF ne contient pas de demande de prêt valide.",
        "es": "Fallido: El PDF no contiene una solicitud de préstamo válida.",
        "en-gb": "Failed: PDF does not contain a valid Loan Application Sheet."
    },
    "INGEST_ERR_PARSE_ERROR": {
        "it": "Fallito: PDF corrotto, crittografato o illeggibile.",
        "de": "Fehlgeschlagen: PDF ist beschädigt, verschlüsselt oder unlesbar.",
        "fr": "Échec : PDF corrompu, chiffré ou illisible.",
        "es": "Fallido: PDF corrupto, cifrado o ilegible.",
        "en-gb": "Failed: PDF is corrupted, encrypted, or unreadable."
    },
    "INGEST_ERR_UNKNOWN": {
        "it": "Inserimento fallito. Controllare i log del server.",
        "de": "Einfügen fehlgeschlagen. Bitte überprüfen Sie die Serverprotokolle.",
        "fr": "Échec de l’insertion. Veuillez consulter les journaux du serveur.",
        "es": "Error al insertar. Compruebe los registros del servidor.",
        "en-gb": "Insertion failed. Check the server logs."
    },
    "INGEST_ERR_NO_FILE": {
        "it": "Nessun file caricato.",
        "de": "Keine Datei hochgeladen.",
        "fr": "Aucun fichier téléchargé.",
        "es": "Ningún archivo subido.",
        "en-gb": "No file uploaded."
    },
    # VAT: Combined string, browser language term placed first
    "LEGEND_VAT": {
        "it": "P.IVA / USt-IdNr. / N° TVA / NIF / VAT R.No.",
        "de": "USt-IdNr. / P.IVA / N° TVA / NIF / VAT R.No.",
        "fr": "N° TVA / P.IVA / USt-IdNr. / NIF / VAT R.No.",
        "es": "NIF / P.IVA / USt-IdNr. / N° TVA / VAT R. No.",
        "en-gb": "VAT R.No. / P.IVA / USt-IdNr. / N° TVA / NIF"
        },
    # TIN: Combined string, browser language term placed first
    "LEGEND_TIN": {
        "it": "Cod.Fisc. / Steuer-ID / NIR / DNI / NINo",
        "de": "Steuer-ID / Cod.Fisc. / NIR / DNI / NINo",
        "fr": "NIR / Cod.Fisc. / Steuer-ID / DNI / NINo",
        "es": "DNI / Cod.Fisc. / Steuer-ID / NIR / NINo",
        "en-gb": "NINo / Cod.Fisc. / Steuer-ID / NIR / DNI"
        },
    "LEGEND_IBAN": {
        "it": "IBAN",
        "de": "IBAN",
        "fr": "IBAN",
        "es": "IBAN",
        "en-gb": "IBAN"
        },
    "LEGEND_IP": {
        "it": "Indirizzo IP",
        "de": "IP-Adresse",
        "fr": "Adresse IP",
        "es": "Dirección IP",
        "en-gb": "IP Address"
        },
    "LEGEND_COMPANY": {
        "it": "Azienda (denominazione)",
        "de": "Unternehmen (Firmenbezeichnung)",
        "fr": "Entreprise (Dénomination)",
        "es": "Empresa (Denominación)",
        "en-gb": "Company (Company Name)"
        },
    "LEGEND_LOCATION": {
        "it": "Località (sede o filiale)",
        "de": "Ort (Firmensitz oder Filiale)",
        "fr": "Localité (siège social ou agence)",
        "es": "Localidad (domicilio social o sucursal)",
        "en-gb": "Location (registered office or branch)"
        },
    "LEGEND_FULLNAME": {
        "it": "Persona Fisica (Nome e Cognome)",
        "de": "Natürliche Person (Vorname und Nachname)",
        "fr": "Personne physique (Prénom et Nom)",
        "es": "Persona física (Nombre y Apellidos)",
        "en-gb": "Individual (First Name and Last Name)"
        },
    "LEGEND_EMAIL": {
        "it": "Email",
        "de": "E-Mail",
        "fr": "E-mail",
        "es": "Correo",
        "en-gb": "Email"
        },
    "LEGEND_PHONE": {
        "it": "Telefono",
        "de": "Telefon",
        "fr": "Téléphone",
        "es": "Teléfono",
        "en-gb": "Phone"
        },
    "NO_DATA": {
        "it": "Nessuna Domanda di Prestito trovata",
        "de": "Kein Kreditantrag gefunden",
        "fr": "Aucune demande de prêt trouvée",
        "es": "No se ha encontrado ninguna solicitud de préstamo",
        "en-gb": "No loan application found"
        },
    "BDG_OK": {
        "it": "Ok",
        "de": "Ok",
        "fr": "Ok",
        "es": "Ok",
        "en-gb": "OK"
    },
    "BDG_ERR": {
        "it": "Errori",
        "de": "Fehler",
        "fr": "Erreurs",
        "es": "Errores",
        "en-gb": "Errors"
    },
    "BDG_WARN": {
        "it": "Avvisi",
        "de": "Warnungen",
        "fr": "Avertissements",
        "es": "Advertencias",
        "en-gb": "Warnings"
    },
    "ACT_EXPLORE": {
        "it": "Esplora Grafo",
        "de": "Graph Erkunden",
        "fr": "Explorer Graph",
        "es": "Explorar Grafo",
        "en-gb": "Explore Graph"
    },
    "ACT_DETAILS": {
        "it": "Dettagli",
        "de": "Details",
        "fr": "Détails",
        "es": "Detalles",
        "en-gb": "Details"
    },
    "ACT_DOWNLOAD": {
        "it": "Scarica PDF",
        "de": "PDF Herunterladen",
        "fr": "Télécharger PDF",
        "es": "Descargar PDF",
        "en-gb": "Download PDF"
    },
    "ACT_DELETE": {
        "it": "Elimina",
        "de": "Löschen",
        "fr": "Supprimer",
        "es": "Eliminar",
        "en-gb": "Delete"
    },
    "COL_COUNTRY": {
        "it": "Paese",
        "de": "Land",
        "fr": "Pays",
        "es": "País",
        "en-gb": "Country"
    },
    "COL_ACQ_DATE": {
        "it": "Data Acquisizione",
        "de": "Erfassungsdatum",
        "fr": "Date d'acquisition",
        "es": "Fecha de adquisición",
        "en-gb": "Acquisition Date"
    },
    "COL_STATUS": {
        "it": "Stato",
        "de": "Status",
        "fr": "Statut",
        "es": "Estado",
        "en-gb": "Status"
    },
    "COL_ACTION": {
        "it": "Azioni",
        "de": "Aktion",
        "fr": "Action",
        "es": "Acción",
        "en-gb": "Action"
    },
    # The specific list labels referenced by domain_schema.py
    "COL_ID": {
        "it": "N. Domanda",
        "de": "Antrags-Nr.",
        "fr": "N° Demande",
        "es": "N.° Solicitud",
        "en-gb": "Req. No."
    },
    "COL_COMP_NAME": {
        "it": "Azienda",
        "de": "Firma",
        "fr": "Entreprise",
        "es": "Empresa",
        "en-gb": "Company"
    },
    "COL_COMP_VAT": {
        # "it": "Partita IVA",
        # "de": "USt-IdNr.",
        # "fr": "N° TVA",
        # "es": "NIF",
        # "en-gb": "VAT Number"
        "it": "P.IVA (USt-IdNr./N°TVA/NIF/VAT N.)",
        "de": "USt-IdNr. (P.IVA/N°TVA/NIF/VAT N.)",
        "fr": "N° TVA (P.IVA/USt-IdNr./NIF/VAT N.)",
        "es": "NIF (P.IVA/USt-IdNr./N°TVA/VAT N.)",
        "en-gb": "VAT N. (P.IVA/USt-IdNr./N°TVA/NIF)"
    },
    # The Validations and Rules message strings
    "TYPE_SYSTEM": {
        "it": "Applicazione",
        "de": "Anwendung",
        "fr": "Application",
        "es": "Aplicación",
        "en-gb": "Application"
    },
    "REASON_SYSTEM_ERROR": {
        "it": "Errore durante l'esecuzione di '{}': {}",
        "de": "Fehler bei der Ausführung von '{}': {}",
        "fr": "Erreur lors de l'exécution de '{}': {}",
        "es": "Error al ejecutar '{}': {}",
        "en-gb": "Error executing '{}': {}"
    },
    "TYPE_REQUIRED": {
        "it": "Campo obbligatorio",
        "de": "Pflichtfeld",
        "fr": "Champ obligatoire",
        "es": "Campo obligatorio",
        "en-gb": "Required field"
    },
    "REASON_REQUIRED": {
        "it": "Campo obbligatorio mancante",
        "de": "Pflichtfeld fehlt",
        "fr": "Champ obligatoire manquant",
        "es": "Falta un campo obligatorio",
        "en-gb": "Missing required field"
    },
    "TYPE_NUMERIC": {
        "it": "Formato numerico",
        "de": "Numerisches Format",
        "fr": "Format numérique",
        "es": "Formato numérico",
        "en-gb": "Numeric Format"
    },
    "REASON_NUMERIC_INVALID": {
        "it": "Il valore non è un numero valido",
        "de": "Der Wert ist keine gültige Zahl",
        "fr": "La valeur n'est pas un nombre valide",
        "es": "El valor no es un número válido",
        "en-gb": "Value is not a valid number"
    },
    "TYPE_POSITIVE": {
        "it": "Valore positivo",
        "de": "Positiver Wert",
        "fr": "Valeur positive",
        "es": "Valor positivo",
        "en-gb": "Positive Value"
    },
    "REASON_POSITIVE_INVALID": {
        "it": "Il valore deve essere maggiore di zero",
        "de": "Der Wert muss größer als null sein",
        "fr": "La valeur doit être supérieure à zéro",
        "es": "El valor debe ser mayor que cero",
        "en-gb": "Value must be greater than zero"
    },
    "TYPE_EMAIL": {
        "it": "E-mail",
        "de": "E-Mail",
        "fr": "E-mail",
        "es": "Correo electrónico",
        "en-gb": "E-mail"
    },
    "REASON_EMAIL_INVALID": {
        "it": "Indirizzo e-mail non valido",
        "de": "Ungültige E-Mail-Adresse",
        "fr": "Adresse e-mail non valide",
        "es": "Dirección de correo electrónico no válida",
        "en-gb": "Invalid email address"
    },
    "TYPE_IBAN": {
        "it": "IBAN",
        "de": "IBAN",
        "fr": "IBAN",
        "es": "IBAN",
        "en-gb": "IBAN"
    },
    "REASON_IBAN_INVALID": {
        "it": "Checksum IBAN non valido",
        "de": "Ungültige IBAN-Prüfsumme",
        "fr": "Clé de contrôle IBAN non valide",
        "es": "Dígito de control del IBAN no válido",
        "en-gb": "Invalid IBAN checksum"
    },
    "TYPE_BLACKLIST": {
        "it": "Blacklist",
        "de": "Sperrliste",
        "fr": "Liste noire",
        "es": "Lista negra",
        "en-gb": "Blacklist"
    },
    "TYPE_BLACKLIST_IP": {
        "it": "Blacklist IPv4",
        "de": "IPv4-Sperrliste",
        "fr": "Liste noire IPv4",
        "es": "Lista negra de IPv4",
        "en-gb": "IPv4 Blacklist"
    },
    "TYPE_BLACKLIST_IBAN": {
        "it": "Blacklist IBAN",
        "de": "IBAN-Sperrliste",
        "fr": "Liste noire des IBAN",
        "es": "Lista negra de IBAN",
        "en-gb": "IBAN Blacklist"
    },
    "TYPE_BLACKLIST_VAT": {
        "it": {
            "IT": "Blacklist P.IVA italiana",
            "DE": "Blacklist USt-IdNr. tedesca",
            "FR": "Blacklist TVA francese",
            "ES": "Blacklist NIF spagnola",
            "GB": "Blacklist VAT britannica"
        },
        "de": {
            "IT": "Italienische P.IVA-Sperrliste",
            "DE": "Deutsche USt-IdNr.-Sperrliste",
            "FR": "Französische TVA-Sperrliste",
            "ES": "Spanische NIF-Sperrliste",
            "GB": "Britische VAT-Sperrliste"
        },
        "fr": {
            "IT": "Liste noire des P.IVA italiennes",
            "DE": "Liste noire des USt-IdNr. allemandes",
            "FR": "Liste noire des TVA françaises",
            "ES": "Liste noire des NIF espagnols",
            "GB": "Liste noire des VAT britanniques"
        },
        "es": {
            "IT": "Lista negra de P.IVA italianas",
            "DE": "Lista negra de USt-IdNr. alemanas",
            "FR": "Lista negra de TVA francesas",
            "ES": "Lista negra de NIF españoles",
            "GB": "Lista negra de VAT británicas"
        },
        "en-gb": {
            "IT": "Italian P.IVA Blacklist",
            "DE": "German USt-IdNr. Blacklist",
            "FR": "French TVA Blacklist",
            "ES": "Spanish NIF Blacklist",
            "GB": "British VAT Blacklist"
        }
    },
    "TYPE_BLACKLIST_TIN": {
        "it": {
            "IT": "Blacklist Codice Fiscale italiano",
            "DE": "Blacklist Steuer-ID tedesca",
            "FR": "Blacklist NIR francese",
            "ES": "Blacklist DNI spagnola",
            "GB": "Blacklist National Insurance number britannico"
        },
        "de": {
            "IT": "Italienische Codice-Fiscale-Sperrliste",
            "DE": "Deutsche Steuer-ID-Sperrliste",
            "FR": "Französische NIR-Sperrliste",
            "ES": "Spanische DNI-Sperrliste",
            "GB": "Britische National-Insurance-number-Sperrliste"
        },
        "fr": {
            "IT": "Liste noire des Codice Fiscale italiens",
            "DE": "Liste noire des Steuer-ID allemandes",
            "FR": "Liste noire des NIR français",
            "ES": "Liste noire des DNI espagnols",
            "GB": "Liste noire des National Insurance numbers britanniques"
        },
        "es": {
            "IT": "Lista negra de Codice Fiscale italianos",
            "DE": "Lista negra de Steuer-ID alemanas",
            "FR": "Lista negra de NIR franceses",
            "ES": "Lista negra de DNI españoles",
            "GB": "Lista negra de National Insurance numbers británicos"
        },
        "en-gb": {
            "IT": "Italian Codice Fiscale Blacklist",
            "DE": "German Steuer-ID Blacklist",
            "FR": "French NIR Blacklist",
            "ES": "Spanish DNI Blacklist",
            "GB": "UK National Insurance number Blacklist"
        }
    },
    "REASON_IN_BLACKLIST": {
        "it": "Identificativo/valore presente nella blacklist",
        "de": "Kennung/Wert in der Sperrliste gefunden",
        "fr": "Identifiant/valeur trouvé dans la liste noire",
        "es": "Identificador/valor encontrado en la lista negra",
        "en-gb": "Identifier/value found in blacklist"
    },
    "TYPE_DUPLICATE": {
        "it": "Valore duplicato",
        "de": "Doppelter Wert",
        "fr": "Valeur en double",
        "es": "Valor duplicado",
        "en-gb": "Duplicate value"
    },
    "TYPE_DUPLICATE_IP": {
        "it": "IPv4 duplicato",
        "de": "Doppelte IPv4-Adresse",
        "fr": "Adresse IPv4 en double",
        "es": "IPv4 duplicada",
        "en-gb": "Duplicate IPv4"
    },
    "TYPE_DUPLICATE_IBAN": {
        "it": "IBAN duplicato",
        "de": "Doppelte IBAN",
        "fr": "IBAN en double",
        "es": "IBAN duplicado",
        "en-gb": "Duplicate IBAN"
    },
    "TYPE_DUPLICATE_VAT": {
        "it": {
            "IT": "P.IVA italiana duplicata",
            "DE": "USt-IdNr. tedesca duplicata",
            "FR": "TVA francese duplicata",
            "ES": "NIF spagnolo duplicato",
            "GB": "VAT britannica duplicata"
        },
        "de": {
            "IT": "Doppelte italienische P.IVA",
            "DE": "Doppelte deutsche USt-IdNr.",
            "FR": "Doppelte französische TVA",
            "ES": "Doppelte spanische NIF",
            "GB": "Doppelte britische VAT"
        },
        "fr": {
            "IT": "P.IVA italienne en double",
            "DE": "USt-IdNr. allemande en double",
            "FR": "TVA française en double",
            "ES": "NIF espagnol en double",
            "GB": "VAT britannique en double"
        },
        "es": {
            "IT": "P.IVA italiana duplicada",
            "DE": "USt-IdNr. alemana duplicada",
            "FR": "TVA francesa duplicada",
            "ES": "NIF español duplicado",
            "GB": "VAT británica duplicada"
        },
        "en-gb": {
            "IT": "Duplicate Italian P.IVA",
            "DE": "Duplicate German USt-IdNr.",
            "FR": "Duplicate French TVA",
            "ES": "Duplicate Spanish NIF",
            "GB": "Duplicate British VAT"
        }
    },
    "TYPE_DUPLICATE_TIN": {
        "it": {
            "IT": "Codice Fiscale italiano duplicato",
            "DE": "Steuer-ID tedesca duplicata",
            "FR": "NIR francese duplicato",
            "ES": "NIF spagnolo duplicato",
            "GB": "National Insurance number britannico duplicato"
        },
        "de": {
            "IT": "Doppelter italienischer Codice Fiscale",
            "DE": "Doppelte deutsche Steuer-ID",
            "FR": "Doppelte französische NIR",
            "ES": "Doppelte spanische NIF",
            "GB": "Doppelte britische National Insurance number"
        },
        "fr": {
            "IT": "Codice Fiscale italien en double",
            "DE": "Steuer-ID allemande en double",
            "FR": "NIR français en double",
            "ES": "NIF espagnol en double",
            "GB": "National Insurance number britannique en double"
        },
        "es": {
            "IT": "Codice Fiscale italiano duplicado",
            "DE": "Steuer-ID alemana duplicada",
            "FR": "NIR francés duplicado",
            "ES": "NIF español duplicado",
            "GB": "National Insurance number británico duplicado"
        },
        "en-gb": {
            "IT": "Duplicate Italian Codice Fiscale",
            "DE": "Duplicate German Steuer-ID",
            "FR": "Duplicate French NIR",
            "ES": "Duplicate Spanish NIF",
            "GB": "Duplicate UK National Insurance number"
        }
    },
    "REASON_DUPLICATE": {
        "it": "Identificativo/valore duplicato trovato nella stessa scheda di richiesta",
        "de": "Doppelter Bezeichner/Wert in derselben Antragsdatei gefunden",
        "fr": "Identifiant/valeur en double trouvé dans la même fiche de demande",
        "es": "Identificador/valor duplicado encontrado en la misma ficha de solicitud",
        "en-gb": "Duplicate identifier/value found in the same application sheet"
    },
    "TYPE_MISMATCH": {
        "it": "Incongruenza dati",
        "de": "Dateninkonsistenz",
        "fr": "Incohérence des données",
        "es": "Incongruencia de datos",
        "en-gb": "Data inconsistency"
    },
    "TYPE_TIN_MISMATCH": {
        "it": {
            "IT": "Incongruenza dati anagrafici",
            "DE": "",
            "FR": "",
            "ES": "",
            "GB": ""
        },
        "de": {
            "IT": "Inkonsistenz der Personendaten",
            "DE": "",
            "FR": "",
            "ES": "",
            "GB": ""
        },
        "fr": {
            "IT": "Incohérence des données d'identité",
            "DE": "",
            "FR": "",
            "ES": "",
            "GB": ""
        },
        "es": {
            "IT": "Incongruencia de los datos personales",
            "DE": "",
            "FR": "",
            "ES": "",
            "GB": ""
        },
        "en-gb": {
            "IT": "Personal data inconsistency",
            "DE": "",
            "FR": "",
            "ES": "",
            "GB": ""
        }
    },
    "REASON_TIN_MISMATCH": {
        "it": {
            "IT": "Il Codice Fiscale italiano fornito non corrisponde al Nome e Cognome indicati",
            "DE": "",
            "FR": "",
            "ES": "",
            "GB": ""
        },
        "de": {
            "IT": "Der angegebene italienische Codice Fiscale stimmt nicht mit dem angegebenen Vor- und Nachnamen überein",
            "DE": "",
            "FR": "",
            "ES": "",
            "GB": ""
        },
        "fr": {
            "IT": "Le Codice Fiscale italien fourni ne correspond pas au prénom et au nom indiqués",
            "DE": "",
            "FR": "",
            "ES": "",
            "GB": ""
        },
        "es": {
            "IT": "El Codice Fiscale italiano proporcionado no corresponde al nombre y los apellidos indicados",
            "DE": "",
            "FR": "",
            "ES": "",
            "GB": ""
        },
        "en-gb": {
            "IT": "The Italian Codice Fiscale provided does not match the First Name and Last Name provided",
            "DE": "",
            "FR": "",
            "ES": "",
            "GB": ""
        }
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
