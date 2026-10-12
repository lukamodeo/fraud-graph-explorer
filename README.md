# Fraud Graph Explorer

A Django-based proof of concept designed to detect fraud in bank loan applications through link analysis. 

This project allows users to generate synthetic, formally valid loan application sheets (PDF), ingest them, extract identifiers (VAT numbers, Tax Codes, names), and visualize the connections between different applications using an interactive graph. By keeping all countries in the same Vis.js graph, you mimic the behavior of a pan-European Fraud Monitoring tool (like Europol's SIENA or a central bank's AML system). It is highly useful for investigating cases where the same legal representative or applicant appears across multiple different loan applications.

## 🎯 Core Features

### 1. Synthetic Sheet Crafter (`sheet_crafter`) ✅ *Completed*
An interactive lab for generating realistic test data. It features a 100% configuration-driven architecture where a single schema dictionary dictates form generation, data injection, and PDF layout.
*   **5-Country Rule Engine:** Supports IT, DE, FR, ES, and GB. Dynamically applies country-specific format rules for VAT, TIN, and IBAN, differentiating between administrative IDs (DE, ES, GB) and algorithmic IDs (IT, FR).
*   **2D Internationalization (i18n):** A custom, dictionary-based translation engine. The GUI language dynamically adapts to the user's **browser settings**, while the generated PDF structure adapts to the **selected country profile**.
*   **HTMX-Powered UI:** Utilizes HTMX 2.0 for a seamless, single-page application feel. Country dropdown changes instantly fetch new localized labels, apply the correct format rules, and pre-fill the form without full page reloads.
*   **Deterministic TIN Calculation:** Algorithmically calculates valid Tax IDs on the fly. It uses `python-codicefiscale` for Italian Codici Fiscali and a custom deterministic hash function for French NIRs.
*   **Controlled Entropy:** Uses a custom component-pool seed system (128 mathematical combinations) to guarantee graph collisions for testing, rather than using purely random generators.
*   **Interactive Anomaly Injection:** Users can manually edit pre-compiled data. A Bootstrap 5 Modal intercepts name changes for IT/FR profiles to prompt for Sex and DOB, ensuring mathematical consistency before triggering an HTMX TIN recalculation.
*   **HTML-to-PDF Export:** Renders perfectly styled PDFs using `xhtml2pdf` with embedded Base64 letterheads.

### 2. Interactive Graph Explorer (`graph_explorer`) ✅ *Completed*
The main analytical engine. It ingests the generated PDFs, extracts the key identifiers, and maps the relationships using a custom 5-step pipeline, all presented in a modern, **i2 Analyst's Notebook-style** web interface.
*   **1. Extraction (State Machine):** Uses `pdfplumber` to read raw text from PDFs in-memory. A Section-Aware State Machine parses lines top-to-bottom, matching localized labels to `internal_name`s via a reverse-lookup map. It flawlessly handles duplicate labels (e.g., multiple Guarantors) using ordered queues.
*   **2. Normalization:** A dedicated helper function cleans extracted strings for perfect graph linking. It uppercases/strips VAT/TIN/IBANs, prepends country codes to missing IBAN/Phone prefixes, zero-pads IPv4 octets, collapses extra spaces in names, and parses EU decimal formats.
*   **3. Validation Engine (Errors):** A decorator-based `ValidationRegistry` runs explicit `python-stdnum` checksums (VAT, IBAN, TIN) and format checks (Email, IP, Numeric). Implicit `required` checks are also enforced. Results are stored as structured JSON on the `Application` model.
*   **4. Business Rules (Warnings):** A `RuleRegistry` executes field-level and sheet-level rules dynamically. Includes `blacklist` (database-driven), `duplicate` (intra-sheet tag matching), `positive` (amounts), and `tin_name_mismatch` (an IT-specific crossing check that verifies a Codice Fiscale mathematically matches the provided Name/Surname).
*   **5. Graph Population & Save:** Creates `Application` (Sheet Vertex), `Entity` (Identifier Vertex), and `UsesIdentifier` (Edge) records. The normalized value is used for graph linking, while the unnormalized `original_value` is saved on the edge as a forensic audit trail. The original PDF is saved to disk only if ingestion succeeds.

### 3. Analyst Dashboard UI ✅ *Completed*
A sophisticated, 4-tab Bootstrap 5 interface designed to mimic desktop link-analysis tools:
*   **Application Management (Tab 1):** Features a smart upload card with duplicate-detection modals, side-by-side Validation/Warning cards, and an advanced HTMX-driven data table. The table includes an accordion filter system (wildcard search, country, status, date range) that pushes state to the URL, allowing analysts to bookmark or share filtered views.
*   **Graph Explorer (Tab 2):** Renders a dynamic `vis.js` network graph showing a root sheet plus identifiers plus other connected sheets (2 hops at a time). Double-clicking any connected sheet instantly makes it the new root, allowing analysts to seamlessly traverse an infinite web of connections. Includes a toggleable physics engine and interactive legend filters to hide/show specific entity types.
*   **Application Comparison (Tab 3):** A dual-pane view that reconstructs the original PDF layout from database records. The left pane displays the Root Sheet details, while the right pane dynamically loads the details of any Linked Sheet clicked in the graph, providing instant forensic context.
*   **About (Tab 4):** Project information and localization summary.

## 🏗️ Architecture & Tech Stack

*   **Backend:** Django (using a modern `src` layout and a `config` settings module).
*   **PDF Generation:** `xhtml2pdf` for HTML/CSS-to-PDF rendering.
*   **PDF Extraction:** `pdfplumber` for raw text extraction and state-machine parsing.
*   **TIN/ID Validation:** `python-codicefiscale` for Italian ID algorithms, `python-stdnum` for international VAT/IBAN/TIN validation.
*   **Frontend Interactivity:** `HTMX 2.0` for dynamic form updates, Out-Of-Band (OOB) swaps, URL state management, and asynchronous TIN recalculation.
*   **Frontend Styling:** 100% native **Bootstrap 5.3** (locally hosted) combined with Bootstrap Icons. Custom Noto Color Emoji fonts are used for cross-browser country flags in native dropdowns.
*   **Frontend Visualization:** `vis.js` (Network module) for the interactive graph UI, featuring dynamic SVG entity icons and ForceAtlas2 physics.
*   **CLI Management:** Uses `pyproject.toml` with a custom `manage` script for easy path resolution.

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

4. **Run database migrations:**
   ```bash
   manage migrate
   ```

5. **Start the development server:**
   ```bash
   manage runserver
   ```

6. Open your browser and navigate to `http://127.0.0.1:8000/`

## 📂 Project Structure

The project uses a strict Python `src` layout to ensure clean package management.

```text
fraud-graph-explorer/                  
├── pyproject.toml                
├── src/                          
    └── fraud_graph_explorer/          
        ├── manage.py
        ├── config/                <-- Django Project Settings
        ├── domain_schema.py       <-- Shared domain knowledge (Fields, Sections, Enums)
        ├── sheet_crafter/         <-- App 1: Interactive form, TIN recalculation, HTML-to-PDF
        ├── graph_explorer/        <-- App 2: PDF ingestion, Validation Engine, Graph DB, Vis.js UI
        ├── templates/             <-- Centralized HTML templates
        └── static/                <-- CSS, JS, Fonts, and Images
```

## 🛣️ Roadmap / Future Improvements
*   [x] Build the `graph_explorer` ingestion service to parse PDFs back into the database.
*   [x] Implement the Validation and Rule Registry engine for intra-sheet fraud detection.
*   [x] Build the Web Upload View and HTMX Dashboard (Analyst Table with advanced search/filter).
*   [x] Implement the Vis.js infinite 2-hop exploration canvas with dynamic SVG icons.
*   [x] Refactor entire frontend to native Bootstrap 5.3 and HTMX 2.0.
*   [ ] Add fuzzy matching for names during ingestion to catch intentional misspellings.
*   [ ] Export graph findings to a PDF report.
*   [ ] Add machine learning anomaly detection based on graph clustering.
