# Customer Support Assistant

A small Python-based customer support assistant that triages incoming tickets and generates suggested responses using modular "agents" (triage, response, technical/billing/account resolution, feature-request, escalation) and reusable prompt templates. It provides a Streamlit UI for submitting tickets and a backend orchestration layer (back/) that runs the agents and evaluation logic.

### Stack
- Language(s): Python 3.x
- Framework / runtime: Streamlit (UI) + plain Python backend modules
- Notable libraries: see requirements.txt (Streamlit is used by the UI)

## What this is
This repository implements an opinionated prototype for automated customer-support assistance: a Streamlit front-end to submit a ticket and a backend orchestration layer with specialized agents and prompt templates that produce triage decisions and candidate responses. It is aimed at developers building an automated assistant to speed up support workflows and prototype policy-driven response generation.

## How it's organized
Top-level layout:

```
app.py                 # Streamlit UI: ticket submission form and example invocation
requirements.txt       # Python dependencies (install with pip)
back/                  # Backend package
  main.py              # Orchestrator / main backend API used by the UI
  state.py             # Simple runtime state/storage helper
  agents/              # Agent implementations (triage, response, domain-specific)
    triage_agent.py
    response_agent.py
    knowledge_agent.py
    technical_resolution_agent.py
    billing_resolution_agent.py
    account_management_resolution_agent.py
    feature_request_agent.py
    escalation_agent.py
  utils/
    groq/              # GROQ provider and helpers (knowledge/query layer)
      groq_provider.py
      base.py
    prompts/           # Prompt templates used by each agent
      triage_prompt.py
      response_prompt.py
      technical_prompt.py
      billing_prompt.py
      account_prompt.py
      feature_prompt.py
      knowledge_prompt.py
      response_evaluator_prompt.py
      triage_evaluator_prompt.py
    evaluators/        # Response / triage evaluators
      response_evaluator.py
      triage_agent_reponse_evaluator.py
    tools/             # Integrations and helper tools (e.g., Telegram notifier)
      telegram_notifier.py
.gitignore
```

How it fits together:
- The Streamlit script app.py is the interactive entrypoint. It collects a ticket message and calls the backend orchestrator (back.main) to process the ticket.
- back.main exports the orchestration logic used by the UI: it calls the triage agent, invokes the domain-specific resolution agents, consults knowledge via the GROQ provider if needed, and runs evaluators to pick or score candidate responses.
- Prompt templates in back/utils/prompts are reused across agents; evaluators in back/utils/evaluators implement lightweight quality checks on outputs. Tools such as telegram_notifier provide external notifications.

## How to run it (quickstart)
1. Clone the repo:
   git clone https://github.com/JohnnyWorku/customer_support_system.git
   cd customer_support_system

2. Create a venv and install dependencies:
   python -m venv .venv
   source .venv/bin/activate   # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt

3. Run the Streamlit UI:
   streamlit run app.py

4. Submit a ticket in the UI. The UI calls the backend orchestrator which runs triage and response agents and shows the results.

Alternative: invoke the backend programmatically (the Streamlit app uses this pattern). Example (run inside the project or in a Python REPL):
```python
from back.main import app
ticket = {
    "ticket_id": "T-1001",
    "customer_id": "C-500",
    "message": "Describe your issue here..."
}
result = app.invoke(ticket)   # returns the orchestration result used by the UI
print(result)
```

## Configuration / environment
This project connects to external services in some modules (knowledge provider, notification). Configure service credentials as environment variables before running. Typical variables you may need to provide (names may vary depending on your integrations):
- API keys / tokens for any knowledge store or LLM provider used by the GROQ provider or agent code
- TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID (if you enable telegram_notifier)
- Any dataset/project identifiers required by your knowledge provider

Check the provider modules in back/utils/groq and tools/telegram_notifier.py to confirm exact environment variable names and any additional configuration.

## Development notes
- Agents are implemented as separate Python modules in back/agents. To add or extend behavior:
  - Add/modify a prompt in back/utils/prompts/
  - Implement an agent module logic and import it into back/main.py orchestrator
  - Update evaluators in back/utils/evaluators to tune scoring/acceptance thresholds
- The repository uses an in-project state helper (back/state.py) which holds runtime state; for production you would replace this with persistent storage.

## Testing
There are no automated tests included. To test manually:
- Use the Streamlit UI to submit representative tickets and observe triage and response outputs.
- Call agent functions directly from a Python REPL (see the example above).

## Known gaps & recommended improvements
- Persistent storage: back/state.py is a small runtime store — consider persisting tickets and results to a database for auditability.
- Configuration discovery: centralize environment variable and config handling (e.g., a settings.py or pydantic settings model).
- Tests: add unit tests for agents and evaluators to validate prompt changes.
- Security: ensure secrets are loaded from secure vaults in production and not committed to repo.

