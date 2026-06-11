# NALCO Email Intelligence System

An AI-powered internal email intelligence system built for **NALCO (National Aluminium Company Limited)**, a Navratna PSU under India's Ministry of Mines. The system automatically classifies, summarizes, and prioritizes emails using a locally hosted Large Language Model.

---

##  Features

- **AI Email Classification** — Automatically classifies emails into 10 categories: Finance, HR, Systems/IT, Procurement, Operations, Legal/Vigilance, Administration, Safety/Environment, Friends/Family, Others
- **AI Summarization** — Generates concise 2-3 line actionable summaries for each email
- **Urgency Detection** — Flags emails as High, Medium, or Low priority
- **Gmail Integration** — Fetches real emails via Gmail API with OAuth 2.0
- **Auto Polling** — Automatically fetches and classifies new emails every 30 minutes
- **Analytics Dashboard** — Visual charts showing email distribution by category and urgency
- **JWT Authentication** — Secure role-based login (Admin/Employee)
- **Zero Data Leakage** — All AI processing happens locally, no data sent to external servers

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| AI/LLM | Gemma 3B (local) via Ollama |
| Backend | Python, FastAPI, Uvicorn |
| Database | SQLite |
| Frontend | React.js, Recharts, Axios |
| Email | Gmail API, Google OAuth 2.0 |
| Auth | JWT Tokens |
| Scheduler | APScheduler |

---

## 📁 Project Structure

```
nalco-email-intelligence/
├── backend/
│   ├── main.py          # FastAPI app + scheduler
│   ├── classify.py      # Email classification (Gemma LLM)
│   ├── summarize.py     # Email summarization (Gemma LLM)
│   ├── pipeline.py      # Combined AI pipeline
│   ├── gmail_fetch.py   # Gmail API integration
│   ├── database.py      # SQLite operations
│   └── auth.py          # JWT authentication
└── frontend/
    └── src/
        ├── App.js       # Main React dashboard
        └── App.css      # Styling
```
## ⚙️ Setup Instructions

### Prerequisites
- Python 3.12+
- Node.js 18+
- Ollama installed with Gemma 3B model
- Gmail API credentials

### Backend Setup
```bash
cd backend
pip install fastapi uvicorn ollama google-auth-oauthlib google-api-python-client apscheduler python-jose passlib python-multipart
py -m uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Gmail API Setup
1. Create a project on Google Cloud Console
2. Enable Gmail API
3. Create OAuth credentials (Desktop app)
4. Download `credentials.json` and place in `backend/`
5. Run the backend — a browser will open for Gmail authorization

---

## 🔐 Authentication

| Role | Username | Access |
|------|----------|--------|
| Admin | admin | Full dashboard + analytics |
| Employee | employee | Inbox view only |

---

## 🏗️ System Architecture
Gmail API → gmail_fetch.py → pipeline.py → Gemma 3B (Ollama)
↓
SQLite Database
↓
FastAPI REST API
↓
React Dashboard

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /login | JWT authentication |
| GET | /emails | Fetch all classified emails |
| POST | /process | Classify a single email |
| GET | /fetch-now | Trigger immediate Gmail fetch |
## 🏢 About This Project

This project was developed as part of a one-month internship at **NALCO (National Aluminium Company Limited)**, Bhubaneswar — a Navratna PSU under India's Ministry of Mines, placed in the **Systems Department**.

### What I Built
A production-ready, full-stack AI application that solves a real organizational problem — the manual effort employees spend reading, sorting, and prioritizing internal emails. The system:

- Connects to Gmail via OAuth 2.0 and fetches emails automatically every 30 minutes
- Runs each email through a locally hosted **Gemma 3B LLM** (via Ollama) for classification, summarization, and urgency detection — entirely on-premise, zero data leaves the network
- Stores results in a SQLite database with duplicate detection
- Serves the data through a **FastAPI REST API** secured with JWT authentication
- Displays everything on a **React dashboard** with category-wise inbox, urgency color-coding, and analytics charts

### Key Technical Decisions
- **Local LLM over cloud API** — Used Ollama to run Gemma 3B locally instead of OpenAI/Gemini API, ensuring data privacy suitable for a government PSU
- **Few-shot prompt engineering** — Designed structured prompts with category definitions and examples to improve classification accuracy across 10 email categories
- **Auto-polling scheduler** — Integrated APScheduler so new emails are fetched and classified automatically without manual intervention
- **JWT role-based access** — Admin users see full analytics; Employee users see inbox view only

### Production Deployment Path
The system is designed for IMAP integration with any corporate mail server. For production deployment at NALCO, the Gmail API would be replaced with a direct IMAP connection to NALCO's internal mail server — requiring zero changes to the AI pipeline, database, or frontend.

Intern: Shradha Suman Mohapatra   
Department: Systems Department, NALCO  
