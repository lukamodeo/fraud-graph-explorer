# Fraud Graph Explorer

A Django-based proof of concept designed to detect fraud in bank loan applications through link analysis.

This project allows users to generate synthetic, formally valid loan application PDFs, ingest them, extract identifiers (VAT numbers, Tax Codes, names), and visualize the connections between different applications using an interactive graph. By keeping all countries in the same Vis.js graph, you mimic the behavior of a pan-European Fraud Monitoring tool (like Europol's SIENA or a central bank's AML system). It is highly useful for investigating cases where the same legal representative or applicant appears across multiple different loan applications — **even across country borders** (a French TVA on an Italian application, a German Steuer-ID on a British application, etc.).

## 🎯 Core Features

### 1. Synthetic Application Crafter (`sheet_crafter`) ✅ *Completed*
An interactive lab for generating realistic test data. It features a 100% configuration-driven architecture where a single schema dictionary dictates form generation, data injection, and PDF layout.
*   **5-Country Rule Engine:** Supports IT, DE, FR, ES, and GB. Dynamically applies country-specific format rules for VAT, TIN, and IBAN, differentiating between administrative IDs (DE, ES, GB) and algorithmic IDs (IT, FR).
*   **2D Internationalization (i18n):** A custom, dictionary-based translation engine. The GUI language dynamically adapts to the user's **browser settings**, while the generated PDF structure adapts to the **selected country profile**.
*   **HTMX-Powered UI:** Utilizes HTMX 2.0 for a seamless, single-page application feel. Country dropdown changes instantly fetch new localized labels, apply the correct format rules, and pre-fill the form without full page reloads.
*   **Deterministic TIN Calculation:** Algorithmically calculates valid Tax IDs on the fly. It uses `python-codicefiscale` for Italian Codici Fiscali and a custom deterministic hash function for French NIRs.
*   **Custom UK NINo Validator:** Since `python-stdnum` does not include a UK National Insurance Number validator (only UTR), the project ships a custom regex-based validator that mimics stdnum's `is_valid()` API. This makes UK TINs OECD-canonical rather than using UTR.
*   **Robust Decimal Normalization:** The ingestion pipeline parses decimal values from PDFs that may contain currency symbols (`€`, `£`, `$`), currency names ("euro", "pounds", "EUR", "GBP"), and locale-specific separators. Country-aware disambiguation (EU dot-thousands/comma-decimal vs. GB comma-thousands/dot-decimal) is applied.
*   **Controlled Entropy:** Uses a custom component-pool seed system (128 mathematical combinations) to guarantee graph collisions for testing, rather than using purely random generators.
*   **Interactive Anomaly Injection:** Users can manually edit pre-compiled data. A Bootstrap 5 Modal intercepts name changes for IT/FR profiles to prompt for Sex and DOB, ensuring mathematical consistency before triggering an HTMX TIN recalculation.
*   **HTML-to-PDF Export:** Renders perfectly styled PDFs using `xhtml2pdf` with embedded Base64 letterheads.

### 2. Interactive Graph Explorer (`graph_explorer`) ✅ *Completed*
The main analytical engine. It ingests the generated PDFs, extracts the key identifiers, and maps the relationships using a custom 5-step pipeline, all presented in a modern, **i2 Analyst's Notebook-style** web interface.
*   **1. Extraction (State Machine):** Uses `pdfplumber` to read raw text from PDFs in-memory. A Section-Aware State Machine parses lines top-to-bottom, matching localized labels to `internal_name`s via a reverse-lookup map. It flawlessly handles duplicate labels (e.g., multiple Guarantors) using ordered queues.
*   **2. Normalization:** A dedicated helper function cleans extracted strings for perfect graph linking. It uppercases/strips VAT/TIN/IBANs, prepends country codes to missing IBAN/Phone prefixes, zero-pads IPv4 octets, collapses extra spaces in names, and parses EU decimal formats (with currency symbol stripping and locale-aware separator handling).
*   **3. Validation Engine (Errors):** A decorator-based `ValidationRegistry` runs explicit `python-stdnum` checksums (VAT, IBAN, TIN) and format checks (Email, IP, Numeric). VAT/TIN validators accept any of the 5 target countries' formats (not just the application's country), enabling **cross-border identifier validation**.
*   **4. Business Rules (Warnings):** A `RuleRegistry` executes field-level and application-level rules dynamically. Includes `blacklist` (database-driven), `duplicate` (intra-application tag matching with occurrence count), `positive` (amounts), `tin_name_mismatch` (an IT-specific crossing check that verifies a Codice Fiscale mathematically matches the provided Name/Surname — applies based on the **identifier's** country, not the application's), and `foreign_identifier` (warns when an identifier is valid in a country OTHER than the application's country, e.g., a French TVA on an Italian application).
*   **5. Graph Population & Save:** Creates `Application` (Application Vertex), `Entity` (Identifier Vertex with `country_code` populated via `detect_*_country()` dispatchers), and `UsesIdentifier` (Edge) records. The normalized value is used for graph linking, while the unnormalized `original_value` is saved on the edge as a forensic audit trail. The original PDF is saved to disk only if ingestion succeeds. The `raw_data` JSONField on `Application` preserves the exact PDF text for all Sheet-tagged fields, used by the detail view for forensic-grade display.

### 3. Analyst Dashboard UI ✅ *Completed*
A sophisticated, 4-tab Bootstrap 5 interface designed to mimic desktop link-analysis tools:

*   **Application Management (Tab 1):** Features a smart upload card with duplicate-detection modals, side-by-side Validation/Warning cards, and an advanced HTMX-driven data table.
    *   **Advanced Filtering:** Accordion-based filter system with wildcard search (`*`), country, status (ok/err/warn/err_or_warn), date range, and **amount range** (min/max with Decimal coercion and graceful invalid-input handling). All filters push state to the URL via `hx-push-url`, allowing analysts to bookmark or share filtered views.
    *   **Filter Badges:** Active filters are displayed as dismissible badges above the table, with formatted values (locale-aware date formatting via `|date:"SHORT_DATE_FORMAT"`, amount formatting via `|floatformat:0|intcomma` for thousands separators). Clicking the X on a badge clears the corresponding input via `removeFilter()`.
    *   **Count Badge in Header:** The accordion header shows a live count badge with both **Total** (absolute DB count) and **Filtered** (current filter result count), updated via out-of-band (OOB) HTMX swaps whenever filters change.
    *   **Has-Links Column:** A dynamically-computed (per-page, not stored) column shows whether each application has linked applications, using set operations on the `UsesIdentifier` edge table — no DB column needed, automatically reflects new ingests.
    *   **Locale-Aware Amount Column:** The `request_amount` column uses `|floatformat:0|intcomma` from `django.contrib.humanize`, applying locale-aware thousands separators (e.g., `280.000` for Italian users, `280,000` for British users).

*   **Graph Explorer (Tab 2):** Renders a dynamic `vis.js` network graph showing a root application plus identifiers plus other connected applications (2 hops at a time). Double-clicking any connected application instantly makes it the new root, allowing analysts to seamlessly traverse an infinite web of connections. Includes a toggleable physics engine and interactive legend filters to hide/show specific entity types. The graph auto-fits the canvas when Tab 2 becomes visible (handles the "graph stuck in top-left corner" bug when navigating from Tab 3 to Tab 2).

*   **Application Comparison (Tab 3):** A dual-pane view that reconstructs the original PDF layout from database records, using a 50/50 label/value split with monospace font for a data-centric (not PDF-replica) feel.
    *   **Raw Value Display:** Entity-typed fields show the **raw value from the PDF** (preserved on `UsesIdentifier.original_value`), not the normalized form — so currency symbols, original separators, and case are preserved for forensic fidelity. Sheet-tagged fields (like `request_amount`) show from `Application.raw_data` JSONField (preserves the exact PDF text including `€ 280.000,00`).
    *   **Per-Field Alert Badges:** Each field with errors/warnings shows unified circle badges — one per alert, colored by severity (`severity-error-high` = dark red, `severity-warning-medium` = main yellow, etc.), with per-alert-type icons declared on the `@register` decorator (`bi-shield-slash` for blacklist, `bi-files` for duplicate, `bi-flag` for foreign_identifier, etc.). Foreign identifier badges display the country flag emoji instead of an icon. Tooltips show the reason_label + identifier_country + duplicate count.
    *   **Foreign Identifier Flag:** A single flag emoji appears next to the value when the field's identifier is foreign to the application (e.g., 🇫🇷 next to a French TVA on an Italian application), based on the row's `is_foreign` flag — avoids the duplicate-flag bug when multiple alerts fire on the same field.
    *   **Cross-Application Value Highlighting (`applyEvidence`):** When the user clicks a Linked Application node in the graph, the shared entity values (the identifiers that link the two applications) are highlighted in BOTH detail panes simultaneously. Root pane highlights use purple background (`#9b59b6`), linked pane highlights use red background (`#e74c3c`), matching the old i2 Notebook visual language. Each highlight includes a bidirectional-arrow icon (`bi-arrow-left-right`) with a tooltip: "Matched value — present in both applications". Highlights auto-clear and re-apply when the user picks a different linked application.
    *   **Stable Selection Behavior:** Clicking on entity nodes, edges, or empty canvas does NOT deselect the current linked application — only clicking another Linked Application changes the selection. This preserves context when the analyst explores the graph structure.
    *   **Error/Warning Accordions:** Pinned at the bottom of each detail pane, with the same per-alert-type icons prepended to each line (visually linked to the inline badges above). Includes the duplicate count inline (`{count} occurrences`), translated per UI language.
    *   **Empty State:** When no application is selected, the panes show a centered icon + translated message (e.g., "No application selected") via the shared `_empty_state.html` partial.

*   **About (Tab 4):** Project information and localization summary.

### 4. Mixed-Country Identifier Management ✅ *Completed*
A first-class feature: identifiers (VAT, TIN, IBAN) are NOT restricted to the application's own country. A French TVA can appear on an Italian application, a German Steuer-ID on a British application, etc. The system:
*   **Detects** the identifier's country at ingest time via `detect_vat_country()`, `detect_tin_country()`, `detect_iban_country()` dispatchers (in the shared `validators/country_detection.py` module).
*   **Stores** the detected country on `Entity.country_code` for graph-level queries and detail-view flag rendering.
*   **Forwards** the country through `Registry.run()` as `identifier_country` in the alert payload, alongside `count` and `icon`.
*   **Resolves** the `type_label` translation using the alert's `identifier_country` (not the application's country), via the 3D hierarchical translation engine (browser_lang → identifier_country → string). This correctly shows e.g., "Französische TVA-Sperrliste" (German browser, French TVA on Italian application in blacklist) instead of "Italienische P.IVA-Sperrliste" (wrong — application's country).
*   The `section_label` and `field_label` continue to use the **application's** country context (since they describe the application's PDF structure, not the identifier).

### 5. 3D Hierarchical Translation Engine ✅ *Completed*
A custom translation system that handles the complex 2D matrix of (browser_lang × identifier_country) for type_labels, while keeping 1D (browser_lang only) for generic strings like reasons and UI buttons.
*   **`UI_STRINGS` dict:** Contains both 1D entries (lang → string) for generic translations and 3D entries (lang → "ANY" wrapper → country → string) for type_labels.
*   **`"ANY"` sentinel:** Signals "this entry needs the second-level country lookup, don't flatten to a single string". `get_ui_strings()` flattens 1D entries to strings, but leaves "ANY"-wrapped entries as `{country: string}` sub-dicts.
*   **`_localized_lookup()` helper:** Transparently handles both string values (regular 1D) and dict values ("ANY"-wrapped 3D) during alert resolution. Fallback chain: identifier_country → application's country → GB → key itself.
*   **Hand-crafted translations:** Each (browser_lang, identifier_country) combination has its own grammatically-correct translation — no template-based composition that would produce awkward word orders in gendered languages (Italian, French, Spanish, German).

## 🏗️ Architecture & Tech Stack

*   **Backend:** Django (using a modern `src` layout and a `config` settings module).
*   **PDF Generation:** `xhtml2pdf` for HTML/CSS-to-PDF rendering.
*   **PDF Extraction:** `pdfplumber` for raw text extraction and state-machine parsing.
*   **TIN/ID Validation:** `python-codicefiscale` for Italian ID algorithms, `python-stdnum` for international VAT/IBAN/TIN validation, plus a **custom UK NINo validator** (since `stdnum.gb.nino` doesn't exist).
*   **Country Detection:** A shared `validators/country_detection.py` module with `detect_vat_country()`, `detect_tin_country()`, `detect_iban_country()` dispatchers — pure functions, no DB access, callable from both `sheet_crafter` (seed data verification) and `graph_explorer` (ingestion, validation, rules).
*   **Frontend Interactivity:** `HTMX 2.0` for dynamic form updates, Out-Of-Band (OOB) swaps (filter badges, count badges), URL state management (`hx-push-url`), and asynchronous TIN recalculation.
*   **Frontend Styling:** 100% native **Bootstrap 5.3** (locally hosted) combined with Bootstrap Icons. Custom Noto Color Emoji fonts are used for cross-browser country flags in native dropdowns. Custom CSS for severity-gradient badges (6 classes: `severity-{error|warning}-{high|medium|low}`) and evidence-highlight colors (purple for root pane, red for linked pane).
*   **Frontend Visualization:** `vis.js` (Network module) for the interactive graph UI, featuring dynamic SVG entity icons and ForceAtlas2 physics.
*   **Frontend Highlighting:** Custom `applyEvidence()` JS function for cross-application value highlighting via regex word-boundary matching, with cleanup-before-apply pattern to handle re-selection.
*   **CLI Management:** Uses `pyproject.toml` with a custom `manage` script for easy path resolution.
*   **Secrets Management:** `python-dotenv` for loading `.env` (gitignored). A committed `.env.example` template documents required env vars for new contributors.

## 🚀 Getting Started

### Prerequisites
*   Python 3.10+
*   Virtual Environment (venv/pipenv/poetry)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/lukamodeo/fraud-graph-explorer.git
   cd fraud-graph-explorer
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the project in editable mode:**
   *(This installs dependencies and creates the global `manage` CLI command)*
   ```bash
   pip install -e .
   ```

4. **Set up your environment variables:**
   ```bash
   # Copy the example template
   cp .env.example .env

   # Generate a Django SECRET_KEY
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

   # Edit .env and paste the generated key:
   #   SECRET_KEY=<paste-the-key-here>
   #   DEBUG=True
   nano .env
   ```
   The `.env` file is gitignored — your secrets stay local. The `.env.example` template is committed for new contributors.

5. **Run database migrations:**
   ```bash
   manage migrate
   ```

6. **Start the development server:**
   ```bash
   manage runserver
   ```

7. Open your browser and navigate to `http://127.0.0.1:8000/`

## 📂 Project Structure

The project uses a strict Python `src` layout to ensure clean package management.

```text
fraud-graph-explorer/
├── .env.example                    <-- Template for env vars (committed)
├── .env                            <-- Real secrets (gitignored)
├── .gitignore
├── pyproject.toml
├── LICENSE
├── README.md
└── src/
    └── fraud_graph_explorer/
        ├── manage                  <-- CLI entry point (installed via pip install -e .)
        ├── domain_schema.py        <-- Shared domain knowledge (Fields, Sections, Enums, helper functions)
        ├── db.sqlite3
        ├── config/                 <-- Django Project Settings
        ├── graph_explorer/         <-- App 1: PDF ingestion, Validation Engine, Graph DB, Vis.js UI
        ├── sheet_crafter/          <-- App 2: Interactive form, TIN recalculation, HTML-to-PDF
        ├── static/                 <-- CSS, JS, Fonts, and Images
        │   ├── css/
        │   │   ├── crafter.css
        │   │   └── dashboard.css   <-- Custom severity-gradient + evidence-highlight CSS
        │   ├── fonts/
        │   ├── img/
        │   ├── js/
        │   │   ├── graph_explorer.js  <-- applyEvidence(), loadGraphData(), tab-switching, etc.
        │   │   └── sheet_crafter.js
        │   └── vendor/
        │       ├── css/
        │       └── js/
        ├── templates/              <-- Centralized HTML templates (incl. _empty_state.html partial)
        └── validators/             <-- Shared country-detection helpers
            ├── __init__.py
            ├── country_detection.py  <-- detect_vat_country(), detect_tin_country(), detect_iban_country()
            └── uk_nino.py          <-- Custom UK NINo validator (replaces missing stdnum.gb.nino)
```

## 🛣️ Roadmap / Future Improvements
*   [x] Build the `graph_explorer` ingestion service to parse PDFs back into the database.
*   [x] Implement the Validation and Rule Registry engine for intra-application fraud detection.
*   [x] Build the Web Upload View and HTMX Dashboard (Analyst Table with advanced search/filter).
*   [x] Implement the Vis.js infinite 2-hop exploration canvas with dynamic SVG icons.
*   [x] Refactor entire frontend to native Bootstrap 5.3 and HTMX 2.0.
*   [x] Add mixed-country identifier support (VAT/TIN/IBAN accepted in any of 5 countries' formats).
*   [x] Implement `foreign_identifier` rule to warn on cross-border identifiers.
*   [x] Add unified per-field alert badges with severity gradients and per-type icons.
*   [x] Implement `applyEvidence` cross-application value highlighting in detail panes.
*   [x] Add amount range filter and locale-aware amount column formatting.
*   [x] Implement 3D hierarchical translation engine with "ANY" wrapper for mixing-country type_labels.
*   [x] Add custom UK NINo validator (since stdnum.gb.nino doesn't exist).
*   [x] Extend `is_foreign` flag to include IBAN (alongside VAT/TIN).
*   [x] Set up `.env` + `.env.example` workflow for SECRET_KEY management.
*   [ ] Add fuzzy matching for names during ingestion to catch intentional misspellings.
*   [ ] Export graph findings to a PDF report.
*   [ ] Add machine learning anomaly detection based on graph clustering.
*   [ ] Add phone country detection (via international prefix).


