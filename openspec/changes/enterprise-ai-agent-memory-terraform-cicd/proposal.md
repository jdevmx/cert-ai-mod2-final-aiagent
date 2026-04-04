## Why

The BSG Institute Module 2 final project requires a production-ready conversational AI agent in a well-defined complex domain. A 4x4 Off-Road Vehicle Advisor is an ideal domain: it requires synthesizing deep mechanical knowledge (drivetrain physics, differential locks, suspension geometry, tire sizing) with current market data (brands, models, pricing, aftermarket parts), making web search tools genuinely useful and the persistent user profile (rig specs, skill level, use case) critical to personalised advice.

## What Changes

- New full-stack application from scratch (no existing codebase)
- Backend: FastAPI service hosting a LangChain + GPT-4o **4x4 Off-Road Advisor** agent with SSE streaming
- Frontend: React (Vite) SPA with Tailwind CSS and real-time chat UI via SSE
- Database: Firebase Firestore for user rig profiles and persistent conversation history
- Agent tools: Tavily web search for current market data, pricing, trail conditions, and brand news
- Infrastructure: Terraform configuration for GCP (Cloud Run, Secret Manager, IAM)
- CI/CD: GitHub Actions workflows for automated testing (pytest + vitest) and Cloud Run deployment
- Documentation: English-only README and CASE_STUDY covering domain, user profiles, and architectural decisions

## Capabilities

### New Capabilities

- `agent-core`: LangChain ReAct agent (GPT-4o) acting as a 4x4 Off-Road Vehicle Advisor; system prompt dynamically injects the user's rig profile (vehicle, lift, tires, use case, skill level) from Firestore
- `conversation-memory`: Firestore-backed persistent chat history stored as message arrays in a `conversations` collection, keyed by user ID
- `streaming-api`: FastAPI SSE endpoint (`/api/chat/stream`) that streams agent token output to the frontend in real time
- `user-profile`: Firestore `users` collection storing 4x4-specific profile data (vehicle make/model/year, lift height, tire size, locking diffs, primary use: trail/overlanding/daily, skill level) injected into each agent system prompt
- `react-chat-ui`: React + Vite + Tailwind frontend with SSE streaming chat interface and user profile display
- `gcp-infrastructure`: Terraform modules provisioning Cloud Run service, Secret Manager secrets (API keys, Firebase SA), and IAM bindings on GCP
- `ci-cd-pipelines`: GitHub Actions `ci.yml` (pytest + vitest + terraform validate on PRs) and `cd.yml` (deploy to Cloud Run on merge to main)

### Modified Capabilities

## Impact

- Creates the entire project directory structure: `/backend`, `/frontend`, `/infrastructure`, `/.github/workflows`, `/docs`
- Python 3.11 dependencies: FastAPI, uvicorn, LangChain, langchain-openai, langchain-community, firebase-admin, tavily-python, python-dotenv, pytest, pytest-mock, pytest-asyncio
- Node.js dependencies: React 18, Vite, Tailwind CSS, Vitest, @testing-library/react
- Requires GCP project with Cloud Run and Secret Manager APIs enabled
- Secrets needed: `OPENAI_API_KEY`, `TAVILY_API_KEY`, Firebase service account JSON, GCP service account key for GitHub Actions CD
- Terraform remote state should use a GCS bucket
- All code comments, error messages, and documentation must be in English
