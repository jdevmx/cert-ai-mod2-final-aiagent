# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**4x4 Off-Road Vehicle Advisor** — a production-ready conversational AI agent (BSG Institute Module 2 final project). Users chat with a GPT-4o–powered LangChain ReAct agent that gives personalised advice about 4WD systems, differential locks, suspension, tire sizing, and current market options. Advice is tailored to each user's Firestore rig profile (vehicle, lift, tires, skill level).

## Architecture

```
backend/         FastAPI (Python 3.11) + LangChain ReAct agent + GPT-4o
frontend/        React 18 + Vite + Tailwind CSS + native EventSource (SSE)
infrastructure/  Terraform → GCP Cloud Run + Secret Manager + IAM
.github/workflows/  ci.yml (test + lint on PR) | cd.yml (deploy on merge to main)
docs/            README.md + CASE_STUDY.md
ai-specs/        Project spec docs — agents, commands, data model, API spec, standards
openspec/        Change management (proposals, design, tasks) via the openspec CLI
```

### Key data flows

1. **Chat (streaming)**: Browser → `GET /api/chat/stream?user_id=&message=` → FastAPI SSE → LangChain agent streams tokens → EventSource accumulates into a live bubble.
2. **Profile injection**: Before each agent call, `services/user_profile.py` fetches `users/{user_id}` from Firestore; `agent/prompt.py` builds the system prompt from that profile.
3. **Conversation persistence**: `services/conversation.py` loads `conversations/{user_id}` before the agent call and appends the new turn afterward.

### Firestore collections

| Collection | Doc ID | Purpose |
|---|---|---|
| `users` | `user_id` | Rig profile (vehicle, lift, tires, locking_diffs, primary_use, skill_level) |
| `conversations` | `user_id` | Message array `[{role, content, timestamp}]` |

The frontend never touches Firestore directly.

## Commands

### Backend

```bash
cd backend
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000          # dev server
pytest                                          # all tests
pytest tests/test_conversation.py -v           # single file
pytest --cov=. --cov-report=term-missing       # coverage (≥ 80% required)
ruff check . && black .                        # lint + format
```

### Frontend

```bash
cd frontend
npm install
npm run dev            # Vite dev server → http://localhost:5173
npm run test           # Vitest (CI mode)
npm run test:coverage  # coverage (≥ 80% required)
npm run lint && npm run type-check
npm run build          # production build → dist/
```

### Infrastructure

```bash
cd infrastructure
terraform init -backend-config="bucket=<project>-tf-state" -backend-config="prefix=advisor/state"
terraform plan -var="project_id=<project>"
terraform apply -var="project_id=<project>"
```

## Development Rules

- **Keep it simple — no over-engineering.** Solve the problem at hand; no speculative abstractions, no unnecessary layers.
- **Names must make sense.** Every function and variable name must be immediately clear from context. No abbreviations.
- **English only.** All code, comments, error messages, log strings, and docs.
- **Type safety.** Python 3.11 type hints on every function signature; TypeScript strict mode throughout.

## Testing Strategy

**TDD with ≥ 80% coverage. Tests must complete in seconds — no network calls, no timeouts.**

Use **Nullable Infrastructure + Stubs** instead of mocking frameworks (`unittest.mock`, `patch`, `vi.mock`).

### Pattern

Design every service to receive its external dependencies (Firestore client, LLM, search tool) as constructor or function parameters. Provide an in-memory stub implementation for each external dependency. Tests inject the stub directly — no mocking, no patching, instant execution.

- **Backend**: Each external boundary (Firestore, OpenAI, Tavily) has a stub class in `backend/tests/stubs/`. Services accept a dependency interface, not a concrete client.
- **Frontend**: Service functions are passed as hook parameters (defaulting to the real implementation). Tests pass a stub service object with synchronous behavior. `StubEventSource` fires SSE events synchronously so there are no async delays.
- **No timeouts in tests.** A test that must wait for I/O is a test that needs to be redesigned.
- **No real API calls in CI.** Stubs cover 100% of external boundaries.

See `ai-specs/.agents/backend-developer.md` and `ai-specs/specs/backend-standards.mdc` for concrete stub patterns.

## Agent & Spec Files

- `ai-specs/.agents/` — agent definitions for backend-developer, frontend-developer, product-strategy-analyst. Read before planning work in a layer.
- `ai-specs/specs/` — authoritative specs: `api-spec.yml` (OpenAPI), `data-model.md` (Firestore schema), `backend-standards.mdc`, `frontend-standards.mdc`.
- `openspec/changes/` — active change proposals. Use `/opsx:apply` to implement.

## Environment Variables

**Backend** (`.env` in `/backend`): `OPENAI_API_KEY`, `TAVILY_API_KEY`, `FIREBASE_CREDENTIALS_JSON` (base64 service account JSON), `PORT`.

**Frontend** (`.env` in `/frontend`): `VITE_API_URL`, `VITE_DEFAULT_USER_ID`.

## SSE Event Protocol

The `/api/chat/stream` endpoint emits:
- `data: <token>` — partial token
- `event: done\ndata: {}` — stream complete
- `event: error\ndata: {"detail":"..."}` — stream error

The `useSSEChat` hook owns the `EventSource` lifecycle — always close on unmount.
