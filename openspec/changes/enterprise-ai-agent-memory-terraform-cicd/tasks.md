# Tasks — Phase 1 & 2: Backend Core + React Frontend

## Progress: 10/10 tasks complete

### Phase 1 — Backend Core and Firestore Integration

- [x] Task 1: Create `/backend` with FastAPI and LangChain project structure (config, models, main app, requirements, Dockerfile)
- [x] Task 2: Implement Firestore logic — `firebase_client.py`, `services/conversation.py`, `services/user_profile.py` for persistent memory
- [x] Task 3: Create `seed.py` with 3 rich user profiles for testing
- [x] Task 4: Set up LangChain ReAct agent with Tavily search tool — `agent/prompt.py`, `agent/tools/search.py`, `agent/advisor.py`, and API routes `api/routes/chat.py`, `api/routes/users.py`
- [x] Task 5: Unit tests in `backend/tests/` using Nullable Infrastructure stubs (no real API calls)

### Phase 2 — React Frontend & SSE Streaming

- [x] Task 6: Frontend project setup — Vite + React + TypeScript + Tailwind, vite.config.ts with `/api` proxy to localhost:8000
- [x] Task 7: Types and service layer — `src/types.ts`, `chatService.ts` (SSE stream), `userService.ts` (profile + conversation history)
- [x] Task 8: `useSSEChat` hook — SSE lifecycle, token accumulation, done/error events; `App.tsx` with user selector (persisted in localStorage)
- [x] Task 9: UI components — `ChatWindow`, `MessageBubble` (streaming cursor), `ChatInput` (Enter to send), `UserProfilePanel` (rig specs sidebar)
- [x] Task 10: Vitest tests with stubs — `StubEventSource`, `StubUserService`; tests for `useSSEChat`, `MessageBubble`, `ChatWindow`, `UserProfilePanel`
