# \# Computer-Use Automation System

# 

# A browser automation prototype demonstrating live UI discovery, structured workflow artifacts, deterministic replay, safety validation, evidence collection, error handling, and human handoff.

# 

# The system follows this principle:

# 

# > The model discovers the workflow; the generated artifact becomes a reusable capability; deterministic replay executes the workflow consistently.

# 

# \## Features

# 

# \- Browser-based workflow discovery

# \- Structured JSON workflow artifacts

# \- Deterministic replay without an LLM

# \- Safety validation for routes and actions

# \- Evidence logs and screenshots

# \- Error evidence generation

# \- Human handoff state creation

# \- Mock LLM mode for offline execution

# \- Optional OpenAI-powered discovery mode

# 

# \## Project Structure

# 

# ```text

# agent/                 LLM-driven discovery

# app/                   Local banking-style demo application

# artifacts/             Reusable workflow artifacts

# core/                  Safety validation

# evidence/              Logs and screenshots

# handoff/               Human handoff state

# replay/                Deterministic replay engine

# tests/                 Automated tests

# REPORT.md              Architecture and design report

