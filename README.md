# Fraud Graph

A Django-based proof of concept designed to detect fraud in bank loan applications through link analysis. 

This project allows users to generate synthetic, formally valid loan application sheets (PDF), ingest them, extract identifiers (VAT numbers, Tax Codes, names), and visualize the connections between different applications using an interactive graph. It is highly useful for investigating cases where the same legal representative or applicant appears across multiple different loan applications.

## 🎯 Core Features

### 1. Synthetic Sheet Crafter (`sheet_crafter`)
An interactive lab for generating realistic test data. Instead of just generating random data, it provides a UI where users can:
*   **Pre-compile forms** with fake but formally valid data (using `Faker`).
*   **Manually edit** pre-filled components (First Name, Last Name, Birthday) to calculate accurate Tax Codes.
*   **Inject typos and anomalies** (e.g., slightly wrong VAT numbers or Tax Codes) to test the robustness of the ingestion and validation rules.
*   **Export to PDF** using a Markdown-to-PDF pipeline (`markdown_pdf`).

### 2. Interactive Graph Explorer (`graph_explorer`)
The main analytical engine. It ingests the generated PDFs, extracts the key identifiers, and maps the relationships.
*   **PDF Ingestion & Parsing:** Extracts structured data from the two-column PDF recap sheets.
*   **Link Analysis:** Highlights connecting elements, such as the same applicant VAT number or legal representative appearing across multiple sheets.
*   **Infinite Vis.js Exploration:** Renders a dynamic network graph showing a root sheet plus identifiers plus other connected sheets (2 hops at a time). Double-clicking any connected sheet instantly makes it the new root, allowing analysts to seamlessly traverse an infinite web of connections.

## 🏗️ Architecture & Tech Stack

*   **Backend:** Django (using a modern `src` layout and `config` settings module).
*   **Data Generation:** `Faker` for synthetic personal data, `markdown_pdf` for document rendering.
*   **Data Extraction:** `pdfplumber` for extracting text and tables from ingested PDFs.
*   **Frontend Visualization:** `vis.js` (Network module) for the interactive graph UI.
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
   *(This installs dependencies and creates the `manage` CLI command)*
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
        ├── sheet_crafter/         <-- App 1: Interactive form, typo injection, save as PDF
        └── graph_explorer/        <-- App 2: PDF ingestion, Vis.js graph exploration
```

## 🛣️ Roadmap / Future Improvements
*   [ ] Add fuzzy matching for names during ingestion to catch intentional misspellings.
*   [ ] Export graph findings to a PDF report.
*   [ ] Add machine learning anomaly detection based on graph clustering.
