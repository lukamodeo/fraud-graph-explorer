# src/fraud_graph_explorer/graph_explorer/ui_translations.py
from typing import Dict

# Country adjectives, translated per browser UI language.
# Used by resolve_alerts to compose type_labels like "Italian P.IVA Blacklist"
# when the alert's identifier_country is set.
#
# 2D structure: {COUNTRY_CODE: {BROWSER_LANG: translated_adjective}}
# 25 entries (5 countries × 5 languages) — much smaller than pre-resolving
# 5 full ui_strings dicts.
COUNTRY_ADJECTIVES = {
    'IT': {
        'en-gb': 'Italian',
        'it':    'Italiano',
        'de':    'Italienisch',
        'fr':    'Italien',
        'es':    'Italiano',
    },
    'DE': {
        'en-gb': 'German',
        'it':    'Tedesco',
        'de':    'Deutsch',
        'fr':    'Allemand',
        'es':    'Alemán',
    },
    'FR': {
        'en-gb': 'French',
        'it':    'Francese',
        'de':    'Französisch',
        'fr':    'Français',
        'es':    'Francés',
    },
    'ES': {
        'en-gb': 'Spanish',
        'it':    'Spagnolo',
        'de':    'Spanisch',
        'fr':    'Espagnol',
        'es':    'Español',
    },
    'GB': {
        'en-gb': 'British',
        'it':    'Britannico',
        'de':    'Britisch',
        'fr':    'Britannique',
        'es':    'Británico',
    },
}

# Country-specific nouns for VAT/TIN/IBAN identifiers.
# These are language-INVARIANT — they're abbreviations of each country's
# official term (P.IVA = "Partita IVA" in Italian, TVA = "Taxe sur la
# Valeur Ajoutée" in French, etc.). Not translated per browser UI language.
#
# Used by resolve_alerts to compose the type_label using a {noun} placeholder.
# Example: "TVA Blacklist" (FR identifier) vs "P.IVA Blacklist" (IT identifier).
# The country adjective ("French", "Italian") is dropped — the noun itself
# already implies the country (TVA is uniquely French, P.IVA is uniquely Italian).
IDENTIFIER_NOUNS_BY_COUNTRY = {
    'VAT': {
        'IT': 'P.IVA',
        'DE': 'USt-IdNr.',
        'FR': 'TVA',
        'ES': 'NIF',
        'GB': 'VAT Reg.',
    },
    'TIN': {
        'IT': 'Codice Fiscale',
        'DE': 'Steuer-ID',
        'FR': 'NIR',
        'ES': 'DNI',
        'GB': 'UTR',
    },
    'IBAN': {
        # IBAN is the same abbreviation in all 5 countries
        'IT': 'IBAN',
        'DE': 'IBAN',
        'FR': 'IBAN',
        'ES': 'IBAN',
        'GB': 'IBAN',
    },
}

UI_STRINGS = {
    "COUNTRY_FLAGS_NAMES": {
        "it": [('IT', '🇮🇹 Italia'), ('DE', '🇩🇪 Germania'), ('FR', '🇫🇷 Francia'), ('ES', '🇪🇸 Spagna'), ('GB', '🇬🇧 Regno Unito')],
        "de": [('IT', '🇮🇹 Italien'), ('DE', '🇩🇪 Deutschland'), ('FR', '🇫🇷 Frankreich'), ('ES', '🇪🇸 Spanien'), ('GB', '🇬🇧 Vereinigtes Königreich')],
        "fr": [('IT', '🇮🇹 Italie'), ('DE', '🇩🇪 Allemagne'), ('FR', '🇫🇷 France'), ('ES', '🇪🇸 Espagne'), ('GB', '🇬🇧 Royaume-Uni')],
        "es": [('IT', '🇮🇹 Italia'), ('DE', '🇩🇪 Alemania'), ('FR', '🇫🇷 Francia'), ('ES', '🇪🇸 España'), ('GB', '🇬🇧 Reino Unido')],
        "en-gb": [('IT', '🇮🇹 Italy'), ('DE', '🇩🇪 Germany'), ('FR', '🇫🇷 France'), ('ES', '🇪🇸 Spain'), ('GB', '🇬🇧 United Kingdom')]
        },
    "COUNTRY_NAMES": {
        "it": [('IT', 'Italia'), ('DE', 'Germania'), ('FR', 'Francia'), ('ES', 'Spagna'), ('GB', 'Regno Unito')],
        "de": [('IT', 'Italien'), ('DE', 'Deutschland'), ('FR', 'Frankreich'), ('ES', 'Spanien'), ('GB', 'Vereinigtes Königreich')],
        "fr": [('IT', 'Italie'), ('DE', 'Allemagne'), ('FR', 'France'), ('ES', 'Espagne'), ('GB', 'Royaume-Uni')],
        "es": [('IT', 'Italia'), ('DE', 'Alemania'), ('FR', 'Francia'), ('ES', 'España'), ('GB', 'Reino Unido')],
        "en-gb": [('IT', 'Italy'), ('DE', 'Germany'), ('FR', 'France'), ('ES', 'Spain'), ('GB', 'United Kingdom')]
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
        "de": "z.B. Lukas*, DE123*",
        "fr": "ex. Pierre*, FR12*",
        "es": "ej. Juan*, A123*",
        "en-gb": "e.g. John*, GB123*"
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
        "it": "Con Errori",
        "de": "Mit Fehlern",
        "fr": "Avec erreurs",
        "es": "Con errores",
        "en-gb": "With errors"
        },
    "FILTER_STATUS_WARN": {
        "it": "Con Segnalazioni",
        "de": "Mit Warnungen",
        "fr": "Avec alertes",
        "es": "Con alertas",
        "en-gb": "With Alerts"
    },
    "FILTER_STATUS_ERR_OR_WARN": {
        "it": "Con Errori o Segnalazioni",
        "de": "Mit Fehlern oder Warnungen",
        "fr": "Avec erreurs ou alertes",
        "es": "Con errores o alertas",
        "en-gb": "With errors or alerts"
        },
    "FILTER_PREFIX_DATE": {
        "it": "Acquisite",
        "de": "Erfasst",
        "fr": "Reçues",
        "es": "Recibidas",
        "en-gb": "Received"
        },
    "FILTER_START_DATE": {
        "it": "dal",
        "de": "von",
        "fr": "du",
        "es": "desde",
        "en-gb": "from"
        },
    "FILTER_END_DATE": {
        "it": "al",
        "de": "bis",
        "fr": "au",
        "es": "hasta",
        "en-gb": "to"
        },
    "FILTER_PREFIX_AMOUNT": {
        "it": "Importo",
        "de": "Betrag",
        "fr": "Montant",
        "es": "Importe",
        "en-gb": "Amount"
        },
    "FILTER_MIN_AMOUNT": {
        "it": "minimo",
        "de": "Minimum",
        "fr": "minimum",
        "es": "mínimo",
        "en-gb": "minimum"
        },
    "FILTER_MAX_AMOUNT": {
        "it": "massimo",
        "de": "Maximum",
        "fr": "maximum",
        "es": "máximo",
        "en-gb": "maximum"
        },
    "FILTER_BTN_CLEAR": {
        "it": "Rimuovi tutti i Filtri", #TODO
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
        "it": "Segnalazioni",
        "de": "Warnungen",
        "fr": "Alertes",
        "es": "Alertas",
        "en-gb": "Alerts"
        },
    "CARD_NO_ERR": {
        "it": "Nessun errore di validazione",
        "de": "Keine Validierungsfehler",
        "fr": "Aucune erreur de validation",
        "es": "Sin errores de validación",
        "en-gb": "No validation errors"
        },
    "CARD_NO_WARN": {
        "it": "Nessuna segnalazione",
        "de": "Keine Warnungen",
        "fr": "Aucune alerte",
        "es": "Sin alertas",
        "en-gb": "No alerts"
        },
    "CARD_NO_DATA": {
        "it": "Nessuna domanda di prestito selezionata",
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
        "it": "Operazione annullata",
        "de": "Vorgang abgebrochen",
        "fr": "Opération annulée",
        "es": "Operación cancelada",
        "en-gb": "Operation Cancelled"
        },
    "INGEST_ERR_DUPLICATE": {
        "it": "Saltato: {req_num} già inserito",
        "de": "Übersprungen: {req_num} bereits erfasst",
        "fr": "Ignoré : {req_num} déjà intégré",
        "es": "Omitido: {req_num} ya ingestado",
        "en-gb": "Skipped: {req_num} already ingested"
    },
    "INGEST_ERR_INVALID_SHEET": {
        "it": "Fallito: non è una Domanda di Prestito valida",
        "de": "Fehlgeschlagen: Kein gültiger Kreditantrag",
        "fr": "Échec : il n'est pas une demande de prêt valide",
        "es": "Error: no es una solicitud de préstamo válida",
        "en-gb": "Failed: not a valid loan application",
    },
    "INGEST_ERR_PARSE_ERROR": {
        "it": "Fallito: PDF corrotto o crittografato",
        "de": "Fehlgeschlagen: PDF beschädigt oder verschlüsselt",
        "fr": "Échec : le PDF est corrompu ou chiffré",
        "es": "Error: el PDF está dañado o cifrado",
        "en-gb": "Failed: PDF is corrupted or encrypted",
    },
    "INGEST_ERR_UNKNOWN": {
        "it": "Inserimento fallito. Controllare i log",
        "de": "Einfügen fehlgeschlagen. Bitte überprüfen Sie die Protokolle",
        "fr": "Échec de l’insertion. Veuillez consulter les journaux",
        "es": "Error al insertar. Compruebe los registros",
        "en-gb": "Insertion failed. Check the logs"
        },
    "INGEST_ERR_NO_FILE": {
        "it": "Nessun file caricato",
        "de": "Keine Datei hochgeladen",
        "fr": "Aucun fichier téléchargé",
        "es": "Ningún archivo subido",
        "en-gb": "No file uploaded"
    },
    "GRAPH_ROOT_TITLE": {
        "it": "Domanda al centro dell'indagine",
        "de": "Antrag im Zentrum der Untersuchung",
        "fr": "Demande au centre de l’enquête",
        "es": "Solicitud en el centro de la investigación",
        "en-gb": "Application at the Centre of the Investigation"
        },
    "GRAPH_LINKED_TITLE": {
        "it": "Domanda collegata",
        "de": "Verknüpfter Antrag",
        "fr": "Demande liée",
        "es": "Solicitud vinculada",
        "en-gb": "Linked Application"
        },
    "GRAPH_LINKED_VIA": {
        "it": "Presente in",
        "de": "Enthalten in",
        "fr": "Présente dans",
        "es": "Presente en",
        "en-gb": "Present in"
        },
    "GRAPH_LBL_REQ": {
        "it": "Domanda di Prestito",
        "de": "Kreditantrag",
        "fr": "Demande de prêt",
        "es": "Solicitud de préstamo",
        "en-gb": "Loan Application"
        },
    "GRAPH_LBL_BRANCH": {
        "it": "Filiale",
        "de": "Niederlassung",
        "fr": "Agence",
        "es": "Sucursal",
        "en-gb": "Branch"
        },
    "GRAPH_LBL_COMPANY": {
        "it": "Azienda",
        "de": "Unternehmen",
        "fr": "Entreprise",
        "es": "Empresa",
        "en-gb": "Company"
        },
    "GRAPH_LBL_LOC": {
        "it": "Sede legale",
        "de": "Firmensitz",
        "fr": "Siège social",
        "es": "Domicilio social",
        "en-gb": "Registered Office"
        },
    "GRAPH_LBL_VAT": {
        "it": "P.IVA",
        "de": "USt-IdNr.",
        "fr": "N° TVA",
        "es": "NIF",
        "en-gb": "VAT R.No."
        },
    "LEGEND_TITLE": {
        "it": "Legenda & Filtri",
        "de": "Legende & Filter",
        "fr": "Légende & Filtres",
        "es": "Leyenda & Filtros",
        "en-gb": "Legend & Filters"
        },
    "LEGEND_HELP_TEXT": {
        "it": """
            Fai doppio clic su una domanda collegata per renderla il nuovo centro dell'indagine.|
            Seleziona una domanda collegata per caricarne i dettagli per il confronto.|   
            Attiva/disattiva il motore Fisico per disporre meglio i nodi.|
            Nascondi le entità per ridurre il disordine visivo: le domande collegate senza connessioni visibili saranno nascoste automaticamente.
            """,

        "de": """
            Doppelklicke auf einen verknüpften Antrag, um ihn zum neuen Zentrum der Untersuchung zu machen.|
            Wähle einen verknüpften Antrag aus, um seine Details zum Vergleich zu laden.|
            Aktiviere oder deaktiviere die Physik-Engine, um die Knoten besser anzuordnen.|
            Blende Entitäten aus, um die visuelle Unübersichtlichkeit zu reduzieren: Verknüpfte Anträge ohne sichtbare Verbindungen werden automatisch ausgeblendet.
            """,
        "fr": """
            Double-cliquez sur une demande liée pour en faire le nouveau centre de l’enquête.|
            Sélectionnez une demande liée pour charger ses détails en vue de la comparaison.|
            Activez ou désactivez le moteur physique pour mieux disposer les nœuds.|
            Masquez les entités pour réduire l’encombrement visuel : les demandes liées sans connexions visibles seront automatiquement masquées.
            """,
        "es": """
            Haz doble clic en una solicitud vinculada para convertirla en el nuevo centro de la investigación.|
            Selecciona una solicitud vinculada para cargar sus detalles y compararlos.|
            Activa o desactiva el motor físico para distribuir mejor los nodos.|
            Oculta las entidades para reducir el desorden visual: las solicitudes vinculadas sin conexiones visibles se ocultarán automáticamente.
            """,

        "en-gb": """
            Double-click a linked application to make it the new centre of the investigation.|
            Select a linked application to load its details for comparison.|
            Toggle the physics engine on or off to arrange the nodes more effectively.|
            Hide entities to reduce visual clutter: linked applications with no visible connections will be hidden automatically.
            """
        },
    "LEGEND_PHYSICS": {
        "it": "Motore Fisico",
        "de": "Physik-Engine",
        "fr": "Moteur Physique",
        "es": "Motor de Física",
        "en-gb": "Physics Engine"
        },
    "LEGEND_RESET": {
        "it": "Ripristina Vista Grafo",
        "de": "Graphenansicht Zurücksetzen",
        "fr": "Réinitialiser la Vue du Graphe",
        "es": "Restablecer Vista del Grafo",
        "en-gb": "Reset Graph View"
        },
    "DETAIL_ROOT_TITLE": {
        "it": "Domanda al centro dell'indagine",
        "de": "Antrag im Zentrum der Untersuchung",
        "fr": "Demande au centre de l’enquête",
        "es": "Solicitud en el centro de la investigación",
        "en-gb": "Application at the Centre of the Investigation"
        },
    "DETAIL_LINKED_TITLE": {
        "it": "Domanda collegata",
        "de": "Verknüpfter Antrag",
        "fr": "Demande liée",
        "es": "Solicitud vinculada",
        "en-gb": "Linked Application"
        },
    "DETAIL_ROOT_HELP_TEXT": {
        "it": "Seleziona una domanda dall'elenco facendo clic sulle azioni: Grafo oppure Dettagli",
        "de": "Wähle einen Antrag aus der Liste über die Aktionen „Graph“ oder „Details“ aus",
        "fr": "Sélectionnez une demande dans la liste à l’aide des actions « Graphe » ou « Détails »",
        "es": "Selecciona una solicitud de la lista mediante las acciones «Grafo» o «Detalles»",
        "en-gb": "Select an application from the list using the Graph or Details actions"
        },
    "DETAIL_LINKED_HELP_TEXT": {
        "it": "Seleziona una domanda collegata sul Grafo",
        "de": "Wähle einen verknüpften Antrag im Graphen aus",
        "fr": "Sélectionnez une demande liée dans le graphe",
        "es": "Selecciona una solicitud vinculada en el grafo",
        "en-gb": "Select a linked application in the graph"
        },
    "DETAIL_PANE_EMPTY": {
        "it": "Nessuna domanda di prestito selezionata",
        "de": "Kein Kreditantrag ausgewählt",
        "fr": "Aucune demande de prêt sélectionnée",
        "es": "No se ha seleccionado ninguna solicitud de préstamo",
        "en-gb": "No loan application selected"
        },
    "DETAIL_NO_ERR": {
        "it": "Nessun errore di validazione rilevato.",
        "de": "Keine Validierungsfehler erkannt.",
        "fr": "Aucune erreur de validation détectée.",
        "es": "No se detectaron errores de validación.",
        "en-gb": "No validation errors detected."
        },
    "DETAIL_NO_WARN": {
        "it": "Nessuna segnalazione rilevata.",
        "de": "Keine Warnungen erkannt.",
        "fr": "Aucune alerte détectée.",
        "es": "No se detectaron alertas.",
        "en-gb": "No alerts detected."
        },
    "DETAIL_BTN_PDF": {
        "it": "Scarica PDF",
        "de": "PDF Herunterladen",
        "fr": "Télécharger PDF",
        "es": "Descargar PDF",
        "en-gb": "Download PDF"
        },
    "DETAIL_NO_DATA": {
        "it":    "Nessun dato",
        "de":    "Keine Daten",
        "fr":    "Aucune donnée",
        "es":    "Sin datos",
        "en-gb": "No data",
    },
    "DETAIL_FOREIGN": {
        "it":    "Identificativo estero",
        "de":    "Ausländische Kennung",
        "fr":    "Identifiant étranger",
        "es":    "Identificador extranjero",
        "en-gb": "Foreign identifier",
    },
    "DETAIL_INVALID": {
        "it":    "Formato non valido",
        "de":    "Ungültiges Format",
        "fr":    "Format invalide",
        "es":    "Formato no válido",
        "en-gb": "Invalid format",
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
    "COUNT_TOTAL": {
        "it": "Domande totali",
        "de": "Anträge insgesamt",
        "fr": "Nombre total de demandes",
        "es": "Total de solicitudes",
        "en-gb": "Total applications"
        },
    "COUNT_FILTERED": {
        "it": "filtrate",
        "de": "gefiltert",
        "fr": "filtrées",
        "es": "filtradas",
        "en-gb": "filtered",
        },
    "LIST_EMPTY": {
        "it": "Nessuna domanda di prestito trovata",
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
        "it": "Segnalazioni",
        "de": "Warnungen",
        "fr": "Alertes",
        "es": "Alertas",
        "en-gb": "Alerts"
    },
    "HAS_LINKS": {
        "it": "Presenta collegamenti con altre domande",
        "de": "Mit anderen Anträgen verknüpft",
        "fr": "Liée à d’autres demandes",
        "es": "Vinculada a otras solicitudes",
        "en-gb": "Linked to other applications"
        },
    "HAS_NO_LINKS": {
        "it": "Nessun collegamento con altre domande",
        "de": "Keine Verknüpfungen mit anderen Anträgen",
        "fr": "Aucune liaison avec d’autres demandes",
        "es": "Sin vínculos con otras solicitudes",
        "en-gb": "No links to other applications"
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
    "COL_LINKED": {
        "it": "Collegamenti",
        "de": "Verknüpfungen",
        "fr": "Liens",
        "es": "Vínculos",
        "en-gb": "Links"
        },
    "COL_AMOUNT": {
        "it":    "Importo",
        "de":    "Betrag",
        "fr":    "Montant",
        "es":    "Importe",
        "en-gb": "Amount",
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
    "EVIDENCE_LINKED_TOOLTIP": {
        "it": "Rilevata corrispondenza: presente in entrambe le domande",
        "de": "Übereinstimmung erkannt: in beiden Anträgen vorhanden",
        "fr": "Correspondance détectée : présente dans les deux demandes",
        "es": "Coincidencia detectada: presente en ambas solicitudes",
        "en-gb": "Match detected: present in both applications"
        },
    "SEVERITY_LEVEL_LABEL": {
        "it": "Livello di severità",
        "de": "Schweregrad",
        "fr": "Niveau de gravité",
        "es": "Nivel de gravedad",
        "en-gb": "Severity level"
        },

    "SEVERITY_HIGH": {
        "it":    "Alto",
        "de":    "Hoch",
        "fr":    "Élevé",
        "es":    "Alto",
        "en-gb": "High",
    },
    "SEVERITY_MEDIUM": {
        "it":    "Medio",
        "de":    "Mittel",
        "fr":    "Moyen",
        "es":    "Medio",
        "en-gb": "Medium",
    },
    "SEVERITY_LOW": {
        "it":    "Basso",
        "de":    "Niedrig",
        "fr":    "Bas",
        "es":    "Bajo",
        "en-gb": "Low",
    },

    "OCCURRENCES_COUNT": {
        "it":    "occorrenze",
        "de":    "Vorkommen",
        "fr":    "occurrences",
        "es":    "ocurrencias",
        "en-gb": "occurrences",
    },

    "TYPE_SYSTEM": {
        "it": "Errore di sistema",
        "de": "Systemfehler",
        "fr": "Erreur système",
        "es": "Error del sistema",
        "en-gb": "System error"
        },
    "REASON_SYSTEM_ERROR": {
        "it": "'{}': {}",
        "de": "'{}': {}",
        "fr": "'{}': {}",
        "es": "'{}': {}",
        "en-gb": "'{}': {}"
    },

    "TYPE_REQUIRED": {
        "it": "Campo obbligatorio",
        "de": "Pflichtfeld",
        "fr": "Champ obligatoire",
        "es": "Campo obligatorio",
        "en-gb": "Required field"
    },
    "REASON_REQUIRED": {
        "it": "Dato mancante",
        "de": "Fehlende Angabe",
        "fr": "Donnée manquante",
        "es": "Dato obligatorio ausente",
        "en-gb": "Missing data"
        },

    "TYPE_NUMERIC": {
        "it": "Formato numerico",
        "de": "Numerisches Format",
        "fr": "Format numérique",
        "es": "Formato numérico",
        "en-gb": "Numeric Format"
    },
    "REASON_NUMERIC_INVALID": {
        "it": "Numero non valido",
        "de": "Ungültige Zahl",
        "fr": "Nombre non valide",
        "es": "Número no válido",
        "en-gb": "Invalid number"
        },

    "TYPE_POSITIVE": {
        "it": "Valore positivo",
        "de": "Positiver Wert",
        "fr": "Valeur positive",
        "es": "Valor positivo",
        "en-gb": "Positive Value"
    },
    "REASON_POSITIVE_INVALID": {
        "it": "Numero inferiore o uguale a zero",
        "de": "Zahl kleiner oder gleich null",
        "fr": "Nombre inférieur ou égal à zéro",
        "es": "Número menor o igual que cero",
        "en-gb": "Number less than or equal to zero"
        },

    "TYPE_EMAIL": {
        "it": "E-mail",
        "de": "E-Mail",
        "fr": "E-mail",
        "es": "Correo electrónico",
        "en-gb": "E-mail"
    },
    "REASON_EMAIL_INVALID": {
        "it": "Indirizzo non valido",
        "de": "Ungültige Adresse",
        "fr": "Adresse non valide",
        "es": "Dirección no válida",
        "en-gb": "Invalid address"
        },

    "TYPE_IP": {
        "it": "Indirizzo IPv4",
        "de": "IPv4-Adresse",
        "fr": "Adresse IPv4",
        "es": "Dirección IPv4",
        "en-gb": "IPv4 address"
        },
    "REASON_IP_INVALID": {
        "it": "Indirizzo non valido",
        "de": "Ungültige IP-Adresse",
        "fr": "Adresse IP non valide",
        "es": "Dirección IP no válida",
        "en-gb": "Invalid IP address"
        },

    "TYPE_IBAN": {
        "it": {
            "ANY": {
                "IT": "IBAN italiano",
                "DE": "IBAN tedesco",
                "FR": "IBAN francese",
                "ES": "IBAN spagnolo",
                "GB": "IBAN britannico"
                }
            },
        "de": {
            "ANY": {
                "IT": "Italienische IBAN",
                "DE": "Deutsche IBAN",
                "FR": "Französische IBAN",
                "ES": "Spanische IBAN",
                "GB": "Britische IBAN"
                }
            },
        "fr": {
            "ANY": {
                "IT": "IBAN italien",
                "DE": "IBAN allemand",
                "FR": "IBAN français",
                "ES": "IBAN espagnol",
                "GB": "IBAN britannique"
                }
            },
        "es": {
            "ANY": {
                "IT": "IBAN italiano",
                "DE": "IBAN alemán",
                "FR": "IBAN francés",
                "ES": "IBAN español",
                "GB": "IBAN británico"
                }
            },
        "en-gb": {
            "ANY": {
                "IT": "Italian IBAN",
                "DE": "German IBAN",
                "FR": "French IBAN",
                "ES": "Spanish IBAN",
                "GB": "British IBAN"
                }
            }
        },
    "REASON_IBAN_INVALID": {
        "it": "Formato non valido",
        "de": "Ungültiges Format",
        "fr": "Format non valide",
        "es": "Formato no válido",
        "en-gb": "Invalid format"
        },

    "TYPE_TIN": {
        "it": {
            "ANY": {
                "IT": "Codice Fiscale italiano",
                "DE": "Steuer-ID tedesca",
                "FR": "NIR francese",
                "ES": "DNI spagnola",
                "GB": "National Insurance number britannico"
                }
            },
        "de": {
            "ANY": {
                "IT": "Italienischer Codice Fiscale",
                "DE": "Deutsche Steuer-ID",
                "FR": "Französische NIR",
                "ES": "Spanische DNI",
                "GB": "Britische National Insurance number"
                }
            },
        "fr": {
            "ANY": {
                "IT": "Codice Fiscale italien",
                "DE": "Steuer-ID allemande",
                "FR": "NIR français",
                "ES": "DNI espagnol",
                "GB": "National Insurance number britannique"
                }
            },
        "es": {
            "ANY": {
                "IT": "Codice Fiscale italiano",
                "DE": "Steuer-ID alemana",
                "FR": "NIR francés",
                "ES": "DNI español",
                "GB": "National Insurance number británico"
                }
            },
        "en-gb": {
            "ANY": {
                "IT": "Italian Codice Fiscale",
                "DE": "German Steuer-ID",
                "FR": "French NIR",
                "ES": "Spanish DNI",
                "GB": "British National Insurance number"
                }
            }
        },
    "REASON_TIN_INVALID": {
        "it": "Formato non valido",
        "de": "Ungültiges Format",
        "fr": "Format non valide",
        "es": "Formato no válido",
        "en-gb": "Invalid format"
        },

    "TYPE_VAT": {
        "it": {
            "ANY": {
                "IT": "P.IVA italiana",
                "DE": "USt-IdNr. tedesca",
                "FR": "TVA francese",
                "ES": "NIF spagnola",
                "GB": "VAT britannica"
                }
            },
        "de": {
            "ANY": {
                "IT": "Italienische P.IVA",
                "DE": "Deutsche USt-IdNr.",
                "FR": "Französische TVA",
                "ES": "Spanische NIF",
                "GB": "Britische VAT"
                }
            },
        "fr": {
            "ANY": {
                "IT": "P.IVA italienne",
                "DE": "USt-IdNr. allemande",
                "FR": "TVA française",
                "ES": "NIF espagnol",
                "GB": "VAT britannique"
                }
            },
        "es": {
            "ANY": {
                "IT": "P.IVA italiana",
                "DE": "USt-IdNr. alemana",
                "FR": "TVA francesa",
                "ES": "NIF español",
                "GB": "VAT británica"
                }
            },
        "en-gb": {
            "ANY": {
                "IT": "Italian P.IVA",
                "DE": "German USt-IdNr.",
                "FR": "French TVA",
                "ES": "Spanish NIF",
                "GB": "British VAT"
                }
            }
        },
    "REASON_VAT_INVALID": {
        "it": "Formato non valido",
        "de": "Ungültiges Format",
        "fr": "Format non valide",
        "es": "Formato no válido",
        "en-gb": "Invalid format"
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
            "ANY": {
                "IT": "Blacklist P.IVA italiana",
                "DE": "Blacklist USt-IdNr. tedesca",
                "FR": "Blacklist TVA francese",
                "ES": "Blacklist NIF spagnola",
                "GB": "Blacklist VAT britannica"
                }
            },
        "de": {
            "ANY": {
                "IT": "Italienische P.IVA-Sperrliste",
                "DE": "Deutsche USt-IdNr.-Sperrliste",
                "FR": "Französische TVA-Sperrliste",
                "ES": "Spanische NIF-Sperrliste",
                "GB": "Britische VAT-Sperrliste"
                }
            },
        "fr": {
            "ANY": {
                "IT": "Liste noire des P.IVA italiennes",
                "DE": "Liste noire des USt-IdNr. allemandes",
                "FR": "Liste noire des TVA françaises",
                "ES": "Liste noire des NIF espagnols",
                "GB": "Liste noire des VAT britanniques"
                }
            },
        "es": {
            "ANY": {
                "IT": "Lista negra de P.IVA italianas",
                "DE": "Lista negra de USt-IdNr. alemanas",
                "FR": "Lista negra de TVA francesas",
                "ES": "Lista negra de NIF españoles",
                "GB": "Lista negra de VAT británicas"
                }
            },
        "en-gb": {
            "ANY": {
                "IT": "Italian P.IVA Blacklist",
                "DE": "German USt-IdNr. Blacklist",
                "FR": "French TVA Blacklist",
                "ES": "Spanish NIF Blacklist",
                "GB": "British VAT Blacklist"
                }
            }
        },
    "TYPE_BLACKLIST_TIN": {
        "it": {
            "ANY": {
                "IT": "Blacklist Codice Fiscale italiano",
                "DE": "Blacklist Steuer-ID tedesca",
                "FR": "Blacklist NIR francese",
                "ES": "Blacklist DNI spagnola",
                "GB": "Blacklist National Insurance number britannico"
                }
            },
        "de": {
            "ANY": {
                "IT": "Italienische Codice-Fiscale-Sperrliste",
                "DE": "Deutsche Steuer-ID-Sperrliste",
                "FR": "Französische NIR-Sperrliste",
                "ES": "Spanische DNI-Sperrliste",
                "GB": "Britische National-Insurance-number-Sperrliste"
                }
            },
        "fr": {
            "ANY": {
                "IT": "Liste noire des Codice Fiscale italiens",
                "DE": "Liste noire des Steuer-ID allemandes",
                "FR": "Liste noire des NIR français",
                "ES": "Liste noire des DNI espagnols",
                "GB": "Liste noire des National Insurance numbers britanniques"
                }
            },
        "es": {
            "ANY": {
                "IT": "Lista negra de Codice Fiscale italianos",
                "DE": "Lista negra de Steuer-ID alemanas",
                "FR": "Lista negra de NIR franceses",
                "ES": "Lista negra de DNI españoles",
                "GB": "Lista negra de National Insurance numbers británicos"
                }
            },
        "en-gb": {
            "ANY": {
                "IT": "Italian Codice Fiscale Blacklist",
                "DE": "German Steuer-ID Blacklist",
                "FR": "French NIR Blacklist",
                "ES": "Spanish DNI Blacklist",
                "GB": "UK National Insurance number Blacklist"
                }
            }
        },
    "REASON_IN_BLACKLIST": {
        "it": "Presente in blacklist",
        "de": "Auf der Sperrliste",
        "fr": "Figurant sur la liste noire",
        "es": "Incluido en la lista negra",
        "en-gb": "On the blacklist"
        },

    "TYPE_FOREIGN_IBAN": {
        "it": "Codice IBAN estero",
        "de": "Ausländische IBAN",
        "fr": "IBAN étranger",
        "es": "IBAN extranjero",
        "en-gb": "Foreign IBAN"
        },
    "REASON_FOREIGN_IBAN": {
        "it": {
            "ANY": {
                "IT": "Rilevato IBAN italiano",
                "DE": "Rilevato IBAN tedesco",
                "FR": "Rilevato IBAN francese",
                "ES": "Rilevato IBAN spagnolo",
                "GB": "Rilevato IBAN britannico"
                }
            },
        "de": {
            "ANY": {
                "IT": "Erkannte italienische IBAN",
                "DE": "Erkannte deutsche IBAN",
                "FR": "Erkannte französische IBAN",
                "ES": "Erkannte spanische IBAN",
                "GB": "Erkannte britische IBAN"
                }
            },
        "fr": {
            "ANY": {
                "IT": "IBAN italien détecté",
                "DE": "IBAN allemand détecté",
                "FR": "IBAN français détecté",
                "ES": "IBAN espagnol détecté",
                "GB": "IBAN britannique détecté"
                }
            },
        "es": {
            "ANY": {
                "IT": "IBAN italiano detectado",
                "DE": "IBAN alemán detectado",
                "FR": "IBAN francés detectado",
                "ES": "IBAN español detectado",
                "GB": "IBAN británico detectado"
                }
            },
        "en-gb": {
            "ANY": {
                "IT": "Detected Italian IBAN",
                "DE": "Detected German IBAN",
                "FR": "Detected French IBAN",
                "ES": "Detected Spanish IBAN",
                "GB": "Detected British IBAN"
                }
            }
        },

    "TYPE_FOREIGN_VAT": {
        "it": "Codice IVA estero",
        "de": "Ausländische Umsatzsteuer-ID",
        "fr": "Numéro de TVA étranger",
        "es": "Número de IVA extranjero",
        "en-gb": "Foreign VAT number"
        },
    "REASON_FOREIGN_VAT": {
        "it": {
            "ANY": {
                "IT": "Rilevata P.IVA italiana",
                "DE": "Rilevata USt-IdNr. tedesca",
                "FR": "Rilevata TVA francese",
                "ES": "Rilevata NIF spagnola",
                "GB": "Rilevata VAT britannica"
                }
            },
        "de": {
            "ANY": {
                "IT": "Erkannte italienische P.IVA",
                "DE": "Erkannte deutsche USt-IdNr.",
                "FR": "Erkannte französische TVA",
                "ES": "Erkannte spanische NIF",
                "GB": "Erkannte britische VAT"
                }
            },
        "fr": {
            "ANY": {
                "IT": "P.IVA italienne détectée",
                "DE": "USt-IdNr. allemande détectée",
                "FR": "TVA française détectée",
                "ES": "NIF espagnole détectée",
                "GB": "VAT britannique détectée"
                }
            },
        "es": {
            "ANY": {
                "IT": "P.IVA italiana detectada",
                "DE": "USt-IdNr. alemana detectada",
                "FR": "TVA francesa detectada",
                "ES": "NIF española detectada",
                "GB": "VAT británica detectada"
                }
            },
        "en-gb": {
            "ANY": {
                "IT": "Detected Italian P.IVA",
                "DE": "Detected German USt-IdNr.",
                "FR": "Detected French TVA",
                "ES": "Detected Spanish NIF",
                "GB": "Detected British VAT"
                }
            }
        },

    "TYPE_FOREIGN_TIN": {
        "it": "Codice Fiscale (TIN) estero",
        "de": "Ausländische Steueridentifikationsnummer (TIN)",
        "fr": "Numéro d’identification fiscale étranger (TIN)",
        "es": "Número de identificación fiscal extranjero (TIN)",
        "en-gb": "Foreign Tax Identification Number (TIN)"
        },
    "REASON_FOREIGN_TIN": {
        "it": {
            "ANY": {
                "IT": "Rilevato Codice Fiscale italiano",
                "DE": "Rilevata Steuer-ID tedesca",
                "FR": "Rilevato NIR francese",
                "ES": "Rilevata DNI spagnola",
                "GB": "Rilevato National Insurance number britannico"
                }
            },
        "de": {
            "ANY": {
                "IT": "Erkannter italienischer Codice Fiscale",
                "DE": "Erkannte deutsche Steuer-ID",
                "FR": "Erkannter französischer NIR",
                "ES": "Erkannte spanische DNI",
                "GB": "Erkannte britische National Insurance number"
                }
            },
        "fr": {
            "ANY": {
                "IT": "Codice Fiscale italien détecté",
                "DE": "Steuer-ID allemande détectée",
                "FR": "NIR français détecté",
                "ES": "DNI espagnol détecté",
                "GB": "National Insurance number britannique détecté"
                }
            },
        "es": {
            "ANY": {
                "IT": "Codice Fiscale italiano detectado",
                "DE": "Steuer-ID alemana detectada",
                "FR": "NIR francés detectado",
                "ES": "DNI español detectado",
                "GB": "National Insurance number británico detectado"
                }
            },
        "en-gb": {
            "ANY": {
                "IT": "Detected Italian Codice Fiscale",
                "DE": "Detected German Steuer-ID",
                "FR": "Detected French NIR",
                "ES": "Detected Spanish DNI",
                "GB": "Detected British National Insurance number"
                }
            }
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
        "it": {
            "ANY": {
                "IT": "IBAN italiano duplicato",
                "DE": "IBAN tedesco duplicato",
                "FR": "IBAN francese duplicato",
                "ES": "IBAN spagnolo duplicato",
                "GB": "IBAN britannico duplicato"
                }
            },
        "de": {
            "ANY": {
                "IT": "Doppelte italienische IBAN",
                "DE": "Doppelte deutsche IBAN",
                "FR": "Doppelte französische IBAN",
                "ES": "Doppelte spanische IBAN",
                "GB": "Doppelte britische IBAN"
                }
            },
        "fr": {
            "ANY": {
                "IT": "IBAN italien dupliqué",
                "DE": "IBAN allemand dupliqué",
                "FR": "IBAN français dupliqué",
                "ES": "IBAN espagnol dupliqué",
                "GB": "IBAN britannique dupliqué"
                }
            },
        "es": {
            "ANY": {
                "IT": "IBAN italiano duplicado",
                "DE": "IBAN alemán duplicado",
                "FR": "IBAN francés duplicado",
                "ES": "IBAN español duplicado",
                "GB": "IBAN británico duplicado"
                }
            },
        "en-gb": {
            "ANY": {
                "IT": "Duplicate Italian IBAN",
                "DE": "Duplicate German IBAN",
                "FR": "Duplicate French IBAN",
                "ES": "Duplicate Spanish IBAN",
                "GB": "Duplicate British IBAN"
                }
            }
        },
    "TYPE_DUPLICATE_VAT": {
        "it": {
            "ANY": {
                "IT": "P.IVA italiana duplicata",
                "DE": "USt-IdNr. tedesca duplicata",
                "FR": "TVA francese duplicata",
                "ES": "NIF spagnolo duplicato",
                "GB": "VAT britannica duplicata"
                }
            },
        "de": {
            "ANY": {
                "IT": "Doppelte italienische P.IVA",
                "DE": "Doppelte deutsche USt-IdNr.",
                "FR": "Doppelte französische TVA",
                "ES": "Doppelte spanische NIF",
                "GB": "Doppelte britische VAT"
                }
            },
        "fr": {
            "ANY": {
                "IT": "P.IVA italienne en double",
                "DE": "USt-IdNr. allemande en double",
                "FR": "TVA française en double",
                "ES": "NIF espagnol en double",
                "GB": "VAT britannique en double"
                }
            },
        "es": {
            "ANY": {
                "IT": "P.IVA italiana duplicada",
                "DE": "USt-IdNr. alemana duplicada",
                "FR": "TVA francesa duplicada",
                "ES": "NIF español duplicado",
                "GB": "VAT británica duplicada"
                }
            },
        "en-gb": {
            "ANY": {
                "IT": "Duplicate Italian P.IVA",
                "DE": "Duplicate German USt-IdNr.",
                "FR": "Duplicate French TVA",
                "ES": "Duplicate Spanish NIF",
                "GB": "Duplicate British VAT"
                }
            }
        },
    "TYPE_DUPLICATE_TIN": {
        "it": {
            "ANY": {
                "IT": "Codice Fiscale italiano duplicato",
                "DE": "Steuer-ID tedesca duplicata",
                "FR": "NIR francese duplicato",
                "ES": "NIF spagnolo duplicato",
                "GB": "National Insurance number britannico duplicato"
                }
            },
        "de": {
            "ANY": {
                "IT": "Doppelter italienischer Codice Fiscale",
                "DE": "Doppelte deutsche Steuer-ID",
                "FR": "Doppelte französische NIR",
                "ES": "Doppelte spanische NIF",
                "GB": "Doppelte britische National Insurance number"
                }
            },
        "fr": {
            "ANY": {
                "IT": "Codice Fiscale italien en double",
                "DE": "Steuer-ID allemande en double",
                "FR": "NIR français en double",
                "ES": "NIF espagnol en double",
                "GB": "National Insurance number britannique en double"
                }
            },
        "es": {
            "ANY": {
                "IT": "Codice Fiscale italiano duplicado",
                "DE": "Steuer-ID alemana duplicada",
                "FR": "NIR francés duplicado",
                "ES": "NIF español duplicado",
                "GB": "National Insurance number británico duplicado"
                }
            },
        "en-gb": {
            "ANY": {
                "IT": "Duplicate Italian Codice Fiscale",
                "DE": "Duplicate German Steuer-ID",
                "FR": "Duplicate French NIR",
                "ES": "Duplicate Spanish NIF",
                "GB": "Duplicate UK National Insurance number"
                }
            }
        },
    "REASON_DUPLICATE_VALUE": {
        "it": "Rilevato duplicato nella stessa richiesta",
        "de": "Doppelter Wert im selben Antrag erkannt",
        "fr": "Valeur en double détectée dans la même demande",
        "es": "Valor duplicado detectado en la misma solicitud",
        "en-gb": "Duplicate value detected in the same application"
    },

    "TYPE_MISMATCH": {
        "it": "Incongruenza dati",
        "de": "Dateninkonsistenz",
        "fr": "Incohérence des données",
        "es": "Incongruencia de datos",
        "en-gb": "Data inconsistency"
    },
    "TYPE_TIN_NAME_MISMATCH": {
        "it": {
            "ANY": {
                "IT": "Incongruenza dati anagrafici",
                "DE": "",
                "FR": "",
                "ES": "",
                "GB": ""
                }
            },
        "de": {
            "ANY": {
                "IT": "Inkonsistenz der Personendaten",
                "DE": "",
                "FR": "",
                "ES": "",
                "GB": ""
                }
            },
        "fr": {
            "ANY": {
                "IT": "Incohérence des données d'identité",
                "DE": "",
                "FR": "",
                "ES": "",
                "GB": ""
                }
            },
        "es": {
            "ANY": {
                "IT": "Incongruencia de los datos personales",
                "DE": "",
                "FR": "",
                "ES": "",
                "GB": ""
                }
            },
        "en-gb": {
            "ANY": {
                "IT": "Personal data inconsistency",
                "DE": "",
                "FR": "",
                "ES": "",
                "GB": ""
                }
            }
        },
    "REASON_TIN_NAME_MISMATCH": {
        "it": {
            "ANY": {
                "IT": "Codice Fiscale italiano non corrispondente a Nome e Cognome",  # TODO
                "DE": "",
                "FR": "",
                "ES": "",
                "GB": ""
                }
            },
        "de": {
            "ANY": {
                "IT": "Der angegebene italienische Codice Fiscale stimmt nicht mit dem angegebenen Vor- und Nachnamen überein",
                "DE": "",
                "FR": "",
                "ES": "",
                "GB": ""
                }
            },
        "fr": {
            "ANY": {
                "IT": "Le Codice Fiscale italien fourni ne correspond pas au prénom et au nom indiqués",
                "DE": "",
                "FR": "",
                "ES": "",
                "GB": ""
                }
            },
        "es": {
            "ANY": {
                "IT": "El Codice Fiscale italiano proporcionado no corresponde al nombre y los apellidos indicados",
                "DE": "",
                "FR": "",
                "ES": "",
                "GB": ""
                }
            },
        "en-gb": {
            "ANY": {
                "IT": "The Italian Codice Fiscale provided does not match the First Name and Last Name provided",
                "DE": "",
                "FR": "",
                "ES": "",
                "GB": ""
                }
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
                final_value = context_dict.get(pdf_cc, context_dict.get("GB", ""))
                if final_value:
                    # Regular 2D entry — found the sheet's country string
                    flat_dict[key] = final_value
                else:
                    # NEW: "ANY"-wrapped entry — fall back to the country→string sub-dict
                    # Used for TYPE_* translations where the lookup needs to use the
                    # alert's identifier_country, not the sheet's country.
                    # Returns the inner {country: string} dict for resolve_alerts to do
                    # the second-level lookup.
                    flat_dict[key] = context_dict.get("ANY", "")
            else:
                flat_dict[key] = ""
        else:
            # It's 1D: Get the string directly based on browser language
            flat_dict[key] = val.get(lang, val.get("en-gb", ""))

    return flat_dict
