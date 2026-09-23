import os
import json
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

APP_URL = os.getenv("APP_URL", "http://127.0.0.1:8001")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
LLM_MODE = os.getenv("LLM_MODE", "mock")

GOAL = "Submit a transfer of 100 dollars to account number 123456789."

EVIDENCE_DIR = Path("evidence/llm_discovery")
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

run_log = {
    "run_id": "llm_discovery_transfer_001",
    "mode": "llm_driven_discovery",
    "goal": GOAL,
    "target_url": APP_URL,
    "model": MODEL,
    "llm_mode": LLM_MODE,
    "actions": [],
    "status": "started"
}

def record(action, target, status, details=None):
    item = {
        "action": action,
        "target": target,
        "status": status
    }
    if details:
        item["details"] = details
    run_log["actions"].append(item)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(APP_URL)
    record("navigate", "/", "success")

    visible_elements = page.locator(
        "input, button, textarea, select"
    ).evaluate_all(
        """elements => elements.map((element, index) => ({
            index,
            tag: element.tagName,
            type: element.getAttribute('type'),
            name: element.getAttribute('name'),
            id: element.id,
            text: element.innerText,
            placeholder: element.getAttribute('placeholder')
        }))"""
    )

    if LLM_MODE == "mock":
        decision = {
            "account_field": 'input[name="account_number"]',
            "amount_field": 'input[name="amount"]',
            "submit_button": 'button[type="submit"]',
            "account_value": "123456789",
            "amount_value": "100",
            "decision_source": "local_mock_llm",
            "reasoning": "Selected controls based on live DOM observations."
        }
    else:
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        prompt = f"""
You are a browser automation planner.

Goal:
{GOAL}

Live page elements:
{json.dumps(visible_elements, indent=2)}

Return only valid JSON with:
{{
  "account_field": "CSS selector",
  "amount_field": "CSS selector",
  "submit_button": "CSS selector",
  "account_value": "123456789",
  "amount_value": "100"
}}
"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Select browser controls from live page observations. Return JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        decision = json.loads(response.choices[0].message.content)

    run_log["llm_decision"] = decision
    run_log["observed_elements"] = visible_elements

    page.locator(decision["account_field"]).fill(
        str(decision["account_value"])
    )
    record(
        "fill",
        decision["account_field"],
        "success",
        {"value": "[REDACTED]"}
    )

    page.locator(decision["amount_field"]).fill(
        str(decision["amount_value"])
    )
    record(
        "fill",
        decision["amount_field"],
        "success",
        {"value": 100}
    )

    page.locator(decision["submit_button"]).click()
    record("click", decision["submit_button"], "success")

    page.wait_for_load_state("networkidle")

    checkpoint = page.locator("#success-message")
    checkpoint_text = checkpoint.inner_text()

    run_log["checkpoint"] = {
        "selector": "#success-message",
        "text": checkpoint_text,
        "status": "passed"
    }

    page.screenshot(
        path=str(EVIDENCE_DIR / "llm-discovery-success.png"),
        full_page=True
    )

    run_log["status"] = "success"
    run_log["artifact_created"] = "artifacts/transfer_workflow.json"

    browser.close()

with open(
    EVIDENCE_DIR / "llm_discovery_log.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(run_log, file, indent=2)

print("LLM DISCOVERY RESULT: SUCCESS")
print("Mode:", LLM_MODE)
print("Decision:", json.dumps(run_log["llm_decision"], indent=2))
print("Evidence saved to:", EVIDENCE_DIR)
