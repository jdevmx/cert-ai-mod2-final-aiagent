# 4x4 Off-Road Vehicle Advisor

A production-ready conversational AI agent that gives personalised advice about 4WD systems, differential locks, suspension, tire sizing, and current market options. Advice is tailored to each user's rig profile stored in Firestore.

> BSG Institute — Module 2 Final Project

---

## Architecture

```
backend/           FastAPI (Python 3.11) + LangChain ReAct agent + GPT-4o
frontend/          React 18 + Vite + Tailwind CSS + SSE streaming chat UI
infrastructure/    Terraform → GCP Cloud Run + Secret Manager + IAM
.github/workflows/ ci.yml (test + lint) | cd.yml (deploy on merge to main)
docs/              README + CASE_STUDY
ai-specs/          OpenAPI spec, data model, agent & standards docs
```

### Key data flows

1. **Chat (streaming)** — Browser → `GET /api/chat/stream?user_id=&message=` → FastAPI SSE → LangChain agent streams tokens → EventSource accumulates into a live bubble.
2. **Profile injection** — Before each agent call, `services/user_profile.py` fetches `users/{user_id}` from Firestore; `agent/prompt.py` builds the system prompt from that profile.
3. **Conversation persistence** — `services/conversation.py` loads `conversations/{user_id}` before the agent call and appends the new turn afterward.

### Firestore collections

| Collection      | Doc ID    | Purpose                                                                 |
|-----------------|-----------|-------------------------------------------------------------------------|
| `users`         | `user_id` | Rig profile (vehicle, lift, tires, locking_diffs, primary_use, skill_level) |
| `conversations` | `user_id` | Message array `[{role, content, timestamp}]`                            |

---

## Getting started

### Prerequisites

- Python 3.11
- Node.js 20+
- A GCP project with Cloud Run and Secret Manager APIs enabled
- Firebase project (Firestore in Native mode)
- OpenAI API key
- Tavily API key

### Backend

```bash
cd backend
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Copy and fill in environment variables
cp .env.example .env

uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install

# Copy and fill in environment variables
cp .env.example .env

npm run dev   # http://localhost:5173
```

### Infrastructure

```bash
cd infrastructure
terraform init -backend-config="bucket=<project>-tf-state" -backend-config="prefix=advisor/state"
terraform plan  -var="project_id=<project>"
terraform apply -var="project_id=<project>"
```

---

## Environment variables

**Backend** (`backend/.env`):

| Variable                   | Description                                    |
|----------------------------|------------------------------------------------|
| `OPENAI_API_KEY`           | OpenAI API key                                 |
| `TAVILY_API_KEY`           | Tavily search API key                          |
| `FIREBASE_CREDENTIALS_JSON`| Base64-encoded Firebase service account JSON   |
| `PORT`                     | Server port (default `8000`)                   |

**Frontend** (`frontend/.env`):

| Variable              | Description                          |
|-----------------------|--------------------------------------|
| `VITE_API_URL`        | Backend base URL                     |
| `VITE_DEFAULT_USER_ID`| Default user ID for development      |

---

## API

Full OpenAPI spec at [`ai-specs/specs/api-spec.yml`](ai-specs/specs/api-spec.yml).

Key endpoints:

| Method | Path                                  | Description                        |
|--------|---------------------------------------|------------------------------------|
| GET    | `/api/chat/stream`                    | SSE streaming chat                 |
| POST   | `/api/chat`                           | Non-streaming chat                 |
| GET    | `/api/users/{user_id}/profile`        | Get rig profile                    |
| PUT    | `/api/users/{user_id}/profile`        | Create / update rig profile        |
| GET    | `/api/users/{user_id}/conversations`  | Get conversation history           |
| DELETE | `/api/users/{user_id}/conversations`  | Clear conversation history         |
| GET    | `/health`                             | Health check (Cloud Run probe)     |

### SSE event protocol

```
data: <token>                      # partial token
event: done\ndata: {}              # stream complete
event: error\ndata: {"detail":"…"} # stream error
```

---

## Testing

```bash
# Backend (≥ 80% coverage required)
cd backend
pytest --cov=. --cov-report=term-missing

# Frontend (≥ 80% coverage required)
cd frontend
npm run test:coverage
```

Tests use **Nullable Infrastructure + Stubs** — no mocking frameworks, no network calls, instant execution.

---

## CI/CD

| Workflow               | Trigger              | Actions                                    |
|------------------------|----------------------|--------------------------------------------|
| `.github/workflows/ci.yml` | Pull request     | pytest + vitest + ruff + terraform validate |
| `.github/workflows/cd.yml` | Merge to `main`  | Build + push image → deploy to Cloud Run   |

---

## License

MIT
