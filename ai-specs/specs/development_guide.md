# Development Guide

Step-by-step instructions for setting up the development environment and running tests
for the 4x4 Off-Road Vehicle Advisor AI agent.

## Prerequisites

Ensure the following are installed before starting:

- **Python 3.11** (use `pyenv` or `asdf` to manage versions)
- **Node.js 20 LTS** and **npm 10+**
- **Git**
- **Google Cloud SDK** (`gcloud`) — for GCP deployment
- **Terraform 1.7+** — for infrastructure provisioning
- A **GCP project** with billing enabled

---

## 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <repo-name>
```

---

## 2. Environment Variables

### Backend (`/backend/.env`)

```env
# OpenAI
OPENAI_API_KEY=sk-...

# Tavily Search
TAVILY_API_KEY=tvly-...

# Firebase — base64-encoded service account JSON
# Generate: base64 -i serviceAccount.json | tr -d '\n'
FIREBASE_CREDENTIALS_JSON=eyJ0eXBlIjoi...

# GCP Project (for Cloud Run deployment)
GCP_PROJECT_ID=your-gcp-project-id

# Server
PORT=8000
```

### Frontend (`/frontend/.env`)

```env
VITE_API_URL=http://localhost:8000
VITE_DEFAULT_USER_ID=dev_user_001
```

---

## 3. Backend Setup (FastAPI + LangChain)

```bash
cd backend

# Create and activate virtual environment
python3.11 -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Start the development server (with hot reload)
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.
Interactive API docs at `http://localhost:8000/docs`.

### Key dependencies

```
fastapi
uvicorn[standard]
langchain
langchain-openai
langchain-community
tavily-python
firebase-admin
pydantic-settings
python-dotenv
```

### Running Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=term-missing

# Run a specific test file
pytest tests/test_conversation.py -v
```

Tests use `unittest.mock` and `pytest-mock` to mock OpenAI, Firebase, and Tavily.
No real API calls are made during `pytest`.

---

## 4. Frontend Setup (React + Vite + Tailwind)

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`.

### Key dependencies

```json
{
  "react": "^18.3.0",
  "vite": "^5.0.0",
  "tailwindcss": "^3.4.0",
  "typescript": "^5.4.0"
}
```

### Running Frontend Tests

```bash
cd frontend

# Run unit tests (Vitest)
npm run test

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage
```

Tests use `vitest` and `@testing-library/react`. SSE and `fetch` are mocked with `vi.stubGlobal`.

---

## 5. Infrastructure Setup (Terraform + GCP)

### One-time GCP setup

```bash
# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com secretmanager.googleapis.com

# Create GCS bucket for Terraform state
gsutil mb -l us-central1 gs://YOUR_PROJECT_ID-tf-state
```

### Provision infrastructure

```bash
cd infrastructure

# Initialize Terraform with remote state backend
terraform init \
  -backend-config="bucket=YOUR_PROJECT_ID-tf-state" \
  -backend-config="prefix=advisor/state"

# Review plan
terraform plan -var="project_id=YOUR_PROJECT_ID"

# Apply
terraform apply -var="project_id=YOUR_PROJECT_ID"
```

Terraform provisions:

- **Cloud Run service** — FastAPI container
- **Secret Manager secrets** — `OPENAI_API_KEY`, `TAVILY_API_KEY`, `FIREBASE_CREDENTIALS_JSON`
- **IAM bindings** — Cloud Run service account access to Secret Manager and Firestore

---

## 6. CI/CD (GitHub Actions)

### Workflows

| File | Trigger | Purpose |
|---|---|---|
| `.github/workflows/ci.yml` | Pull Request | Run pytest, vitest, `terraform validate` |
| `.github/workflows/cd.yml` | Push to `main` | Build Docker image, push to Artifact Registry, deploy to Cloud Run |

### Required GitHub Secrets

Set these in **Repository Settings → Secrets and Variables → Actions**:

| Secret | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI API key |
| `TAVILY_API_KEY` | Tavily search API key |
| `FIREBASE_CREDENTIALS_JSON` | Base64-encoded Firebase service account JSON |
| `GCP_SA_KEY` | Base64-encoded GCP service account JSON for CI/CD |
| `GCP_PROJECT_ID` | GCP project ID |

---

## 7. Running the Full Stack Locally

```bash
# Terminal 1: Backend
cd backend && source .venv/bin/activate && uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend && npm run dev
```

Open `http://localhost:5173` in your browser.

---

## 8. Project Structure Reference

```
.
├── backend/
│   ├── main.py
│   ├── api/routes/
│   ├── agent/
│   ├── services/
│   ├── models/
│   ├── firebase_client.py
│   ├── config.py
│   ├── requirements.txt
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── __tests__/
│   ├── vite.config.ts
│   └── package.json
├── infrastructure/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── .github/workflows/
│   ├── ci.yml
│   └── cd.yml
└── docs/
    ├── README.md
    └── CASE_STUDY.md
```

---

## 9. Code Quality

```bash
# Backend linting (ruff)
cd backend && ruff check .

# Backend formatting (black)
cd backend && black .

# Frontend linting (ESLint)
cd frontend && npm run lint

# Frontend type checking
cd frontend && npm run type-check
```

All code, comments, error messages, and documentation must be written in **English**.
