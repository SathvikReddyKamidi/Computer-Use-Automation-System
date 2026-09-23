# Computer-Use Automation Prototype

A computer-use automation prototype that discovers a workflow through browser interaction, converts the workflow into a reusable structured artifact, and replays it deterministically.

The project uses a local Demo Credit Union application to demonstrate a transfer workflow.

## Core Principle

> The model discovers the workflow.  
> The artifact becomes a reusable capability.  
> Deterministic replay becomes the production execution path.

---

## Features

- Browser-based workflow discovery
- Structured JSON workflow artifacts
- Deterministic workflow replay
- Checkpoint and success validation
- Error handling and failure evidence
- Safety policy validation
- Human handoff and resume tracking
- Visible browser-session intervention
- JSON logs and screenshots
- Optional OpenAI-powered discovery
- Offline mock discovery mode
- Automated test coverage

---

## Project Structure

```text
computer-use-automation/
│
├── agent/
│   └── llm_discovery.py
│
├── app/
│   └── main.py
│
├── artifacts/
│   └── transfer_workflow.json
│
├── core/
│   └── safety.py
│
├── evidence/
│   ├── discovery/
│   ├── errors/
│   ├── llm_discovery/
│   └── replay/
│
├── handoff/
│   ├── active_handoff.json
│   └── handoff.py
│
├── replay/
│   ├── replay_transfer.py
│   └── replay_transfer_backup.py
│
├── tests/
│   ├── create_error_evidence.py
│   ├── test_browser.py
│   ├── test_project.py
│   └── test_transfer.py
│
├── .env.example
├── .gitignore
├── README.md
├── REPORT.md
└── requirements.txt