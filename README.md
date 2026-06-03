<div align="center">

# DocLens
### AI-Powered Document Summarization & Insight Extraction

*Upload any document. Get structured intelligence.*

---

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.57-red?style=flat-square)
![Django](https://img.shields.io/badge/Django-5.2-green?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

</div>

---

## Overview

DocLens is a full-stack AI application that transforms raw documents into structured, actionable intelligence. Users upload a PDF, Word document, CSV, or plain text file, select a domain category, and receive a professionally formatted summary — powered by Groq's Llama 3.3 70B model.

What makes DocLens different from a generic summarizer is **domain-aware prompting** — a Finance document is analysed through the lens of a financial analyst, a Legal document through a legal analyst, a Research document through a research analyst. The AI is given specific instructions per category, producing summaries that are genuinely useful rather than generic.

---

## Features

- **Multi-format support** — PDF, DOCX, CSV, and TXT parsing
- **Domain-aware AI summarization** — 9 category-specific prompt templates (Sales, Education, Technology, Healthcare, Legal, Finance, Operations, Marketing, Research)
- **Structured output** — Executive Summary, Key Points, Action Items, and Data Highlights
- **Adjustable summary style** — Brief, Detailed, or Bullet-only
- **User authentication** — secure registration and login with per-user document storage
- **PDF report export** — download your summary as a professionally formatted PDF
- **Dark / Light theme** — toggle between themes
- **Dashboard** — document history and usage statistics per user

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | Streamlit | Web UI and user interaction |
| Backend | Django + DRF | REST API, authentication, file management |
| AI | Groq API (Llama 3.3 70B) | Document summarization |
| PDF Parsing | PyMuPDF | Extract text from PDFs |
| DOCX Parsing | python-docx | Extract text from Word documents |
| CSV Parsing | pandas | Process spreadsheet data |
| Database | SQLite | Store users and documents |
| PDF Export | ReportLab | Generate downloadable PDF reports |

---

## Project Structure

```
document_service/
│
├── app.py                      # Streamlit frontend — UI, Groq integration, PDF export
├── .env                        # Environment variables (not committed)
├── .gitignore
├── README.md
│
└── smart_summarizer/           # Django backend
    ├── manage.py
    ├── db.sqlite3
    ├── requirements.txt
    │
    ├── smart_summarizer/       # Project configuration
    │   ├── settings.py
    │   └── urls.py
    │
    ├── user/                   # Authentication app
    │   ├── models/             # Custom User model with UUID primary key
    │   ├── views/              # Register, Login, Logout endpoints
    │   ├── serializers/        # Request validation and response formatting
    │   └── urls.py
    │
    └── documents/              # Document processing app
        ├── models/             # Document model with user foreign key
        ├── views/              # Upload and retrieval endpoints
        ├── serializers/        # Document data formatting
        ├── services/           # File parsing logic per format
        └── urls.py
```

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip3
- A free Groq API key — get one at [console.groq.com](https://console.groq.com) (no credit card required)

---

### 1. Clone the repository

```bash
git clone https://github.com/Sarvesh8521/document_service.git
cd document_service
```

---

### 2. Set up the backend

```bash
cd smart_summarizer
pip3 install -r requirements.txt
python3 manage.py migrate
cd ..
```

---

### 3. Install frontend dependencies

```bash
pip3 install streamlit groq python-dotenv reportlab requests
```

---

### 4. Configure your API key

Create a `.env` file in the `document_service` root folder:

```bash
touch .env
```

Add your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

---

### 5. Run the application

DocLens requires two processes running simultaneously — open two terminal windows.

**Terminal 1 — Django backend:**
```bash
cd smart_summarizer
python3 manage.py runserver
```

**Terminal 2 — Streamlit frontend:**
```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Usage

1. **Create an account** on the signup page
2. **Upload a document** — drag and drop or browse (PDF, DOCX, CSV, TXT — up to 200MB)
3. **Select a domain** — choose the category that best matches your document
4. **Choose a summary style** — Brief, Detailed, or Bullet-only
5. **Click Analyse** — the AI reads the document and returns a structured summary
6. **Download** the result as a formatted PDF report

---

## API Reference

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/users/register/` | None | Create a new user account |
| POST | `/api/users/login/` | None | Authenticate and create session |
| POST | `/api/users/logout/` | Required | End session |
| POST | `/api/documents/upload/` | Required | Upload and parse a document |
| GET | `/api/documents/` | Required | List authenticated user's documents |
| GET | `/api/documents/<id>/` | Required | Retrieve a specific document |
| DELETE | `/api/documents/<id>/delete/` | Required | Delete a document |

---

## How the AI Summarization Works

1. The uploaded file is parsed by the Django backend using format-specific parsers (PyMuPDF for PDFs, python-docx for Word files, pandas for CSVs)
2. The extracted plain text is sent to the Streamlit frontend
3. A domain-specific prompt is constructed — combining role instructions, detail level preferences, and the document text
4. The prompt is sent to Groq's API running Llama 3.3 70B
5. The model returns a structured JSON response with four fields: executive summary, key points, action items, and data highlights
6. The response is parsed and rendered in the UI

Each domain has a tailored system prompt. For example, a **Legal** document prompt instructs the model to focus on clauses, obligations, deadlines, and compliance requirements — while a **Finance** prompt focuses on revenue, expenses, ratios, and forecasts.

---

## Team

| Name | Role |
|---|---|
| **Dev Aggarwal** | Frontend — Streamlit UI, Groq AI integration, theme system, PDF export |
| **Sarvesh** | Backend — Django REST API, file parsers, database models, authentication |

---

## Internship Assignment

Built as part of a two-week internship assignment focused on:
- Full-stack Python web development
- LLM integration and prompt engineering
- REST API design with Django
- Collaborative Git-based development workflow
