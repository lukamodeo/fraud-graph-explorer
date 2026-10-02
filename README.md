# Fraud Graph Explorer

A Django-based proof of concept designed to detect fraud in bank loan applications through link analysis. 

This project allows users to generate synthetic, formally valid loan application sheets (PDF), ingest them, extract identifiers (VAT numbers, Tax Codes, names), and visualize the connections between different applications using an interactive graph. It is highly useful for investigating cases where the same legal representative or applicant appears across multiple different loan applications.

## 🎯 Core Features

### 1. Synthetic Sheet Crafter (`sheet_crafter`) ✅ *Completed*
An interactive lab for generating realistic test data. It features a 100% configuration-driven architecture where a single schema dictionary dictates form generation, data injection, and PDF layout.
*   **5-Country Rule Engine:** Supports IT, DE, FR, ES, and GB. Dynamically applies country-specific format rules for VAT, TIN, and IBAN, differentiating between administrative IDs (DE, ES, GB) and algorithmic IDs (IT, FR).
*   **2D Internationalization (i18n):** A custom, dictionary-based translation engine. The GUI language dynamically adapts to the user's **browser settings**, while the generated PDF structure adapts to the **selected country profile**.
*   **HTMX-Powered UI:** Utilizes HTMX for a seamless, single-page application feel. Country dropdown changes instantly fetch new localized labels, apply the correct format rules, and pre-fill the form without full page reloads.
*   **Deterministic TIN Calculation:** Algorithmically calculates valid Tax IDs on the fly. It uses `python-codicefiscale` for Italian Codici Fiscali and a custom deterministic hash function for French NIRs.
*   **Controlled Entropy:** Uses a custom component-pool seed system (128 mathematical combinations) to guarantee graph collisions for testing, rather than using purely random generators.
*   **Interactive Anomaly Injection:** Users can manually edit pre-compiled data. A native HTML `<dialog>` intercepts name changes for IT/FR profiles to prompt for Sex and DOB, ensuring mathematical consistency before triggering an HTMX TIN recalculation.
*   **HTML-to-PDF Export:** Renders perfectly styled PDFs using `xhtml2pdf` with embedded Base64 letterheads.

### 2. Interactive Graph Explorer (`graph_explorer`) 🚧 *Coming Soon*
The main analytical engine. It will ingest the generated PDFs, extract the key identifiers, and map the relationships.
*   **PDF Ingestion & Parsing:** Extracts structured data from the two-column PDF recap sheets.
*   **Link Analysis:** Highlights connecting elements, such as the same applicant VAT number or legal representative appearing across multiple sheets.
*   **Infinite Vis.js Exploration:** Renders a dynamic network graph showing a root sheet plus identifiers plus other connected sheets (2 hops at a time). Double-clicking any connected sheet instantly makes it the new root, allowing analysts to seamlessly traverse an infinite web of connections.

## 🏗️ Architecture & Tech Stack

*   **Backend:** Django (using a modern `src` layout and a `config` settings module).
*   **Frontend Interactivity:** `HTMX` for dynamic form updates, instant language/country switching, and asynchronous TIN recalculation.
*   **PDF Generation:** `xhtml2pdf` for HTML/CSS-to-PDF rendering.
*   **TIN/ID Validation:** `python-codicefiscale` for Italian ID algorithms, `python-stdnum` for international validation (planned for ingestion).
*   **Frontend Styling:** Vanilla CSS, Bootstrap Icons, and custom Noto Color Emoji fonts for cross-browser country flags in native dropdowns.
*   **Frontend Visualization:** `vis.js` (Network module) for the interactive graph UI (planned).
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
        ├── sheet_crafter/         <-- App 1: Interactive form, TIN recalculation, HTML-to-PDF
        ├── graph_explorer/        <-- App 2: PDF ingestion, Vis.js graph exploration (Planned)
        ├── templates/             <-- Centralized HTML templates
        └── static/                <-- CSS, JS, Fonts, and Images
```

## 🛣️ Roadmap / Future Improvements
*   [ ] Build the `graph_explorer` ingestion service to parse PDFs back into the database.
*   [ ] Implement the Vis.js infinite 2-hop exploration canvas.
*   [ ] Add fuzzy matching for names during ingestion to catch intentional misspellings.
*   [ ] Export graph findings to a PDF report.
*   [ ] Add machine learning anomaly detection based on graph clustering.
