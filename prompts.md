### Prompts used for openspec

/opsx:apply "Phase 1: Backend Core and Firestore Integration" --description "
Implement the backend structure based on propose.md and 'Guia_proyecto_agenteia.pdf'. 

### Tasks:
1. Create '/backend' with FastAPI and LangChain setup[cite: 100, 147].
2. Implement Firestore logic in 'firebase/chat_history.py' and 'firebase/clients.py' for persistent memory[cite: 113, 220, 224].
3. Create 'seed.py' with 3 rich user profiles for testing[cite: 47, 136, 335].
4. Set up the LangChain agent with the Tavily search tool in 'agent/agent.py'[cite: 263, 270].
5. Include Unit Tests in '/backend/tests' using pytest and mocks for Firebase/OpenAI.

Document everything in English as per the requirements."


## Phase 2
/opsx:apply "Phase 2: Frontend Development and SSE Streaming" --description "
Develop the React frontend following the 'Guia_proyecto_agenteia.pdf' specifications[cite: 345].

### Tasks:
1. Initialize '/frontend' using Vite and React[cite: 142, 347].
2. Implement the chat interface with a user selector and message history[cite: 363].
3. Integrate Server-Sent Events (SSE) to handle real-time token streaming from the backend[cite: 11, 307].
4. Add Vitest unit tests in '/frontend/src/__tests__' for the main components.

Ensure all UI text and documentation are in English."

## Phase 3

/opsx:apply "Phase 3: Infrastructure as Code and GitHub Actions" --description "
Provision the cloud environment and automation pipelines.

### Tasks:
1. Create '/infrastructure' with Terraform files for GCP Cloud Run and Secret Manager[cite: 405, 407].
2. Configure IAM roles for the service account to access Firestore[cite: 82, 416].
3. Create '.github/workflows/main.yml' to run backend/frontend tests and automate deployment to GCP on push to main.
4. Finalize the README.md and CASE_STUDY.md in English."