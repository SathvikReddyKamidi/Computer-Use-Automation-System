import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from playwright.sync_api import sync_playwright
from handoff.handoff import create_handoff, resume_handoff


ARTIFACT_PATH = PROJECT_ROOT / "artifacts" / "transfer_workflow.json"
LOG_PATH = PROJECT_ROOT / "evidence" / "replay" / "replay_log.json"


def replay_workflow(
    username: str,
    password: str,
    account_number: str,
    amount: float
):
    artifact = json.loads(
        ARTIFACT_PATH.read_text(encoding="utf-8")
    )

    base_url = artifact["target"]["base_url"]

    inputs = {
        "username": username,
        "password": password,
        "account_number": account_number,
        "amount": amount,
    }

    logs = {
        "run_id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "artifact_id": artifact["artifact_id"],
        "artifact_version": artifact["version"],
        "status": "started",
        "steps": [],
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            for step in artifact["steps"]:
                step_id = step["step_id"]
                action = step["action"]

                try:
                    if action == "navigate":
                        page.goto(base_url + step["url"])

                    elif action == "fill":
                        selector = step["target"]["selector"]
                        input_name = step["input"]

                        page.locator(selector).fill(
                            str(inputs[input_name])
                        )

                    elif action == "click":
                        role = step["target"]["role"]
                        name = step["target"]["name"]

                        page.get_by_role(
                            role,
                            name=name
                        ).click()

                        if step_id == "sign_in":
                            page.wait_for_url("**/dashboard")

                    logs["steps"].append({
                        "step_id": step_id,
                        "action": action,
                        "status": "success",
                    })

                except Exception as error:
                    logs["status"] = "handoff_required"
                    logs["error"] = (
                        type(error).__name__ + ": " + str(error)
                    )

                    create_handoff(
                        reason=f"Automation failed: {type(error).__name__}",
                        current_step=step_id,
                        context={
                            "url": page.url,
                            "error": str(error),
                            "message": "Human intervention required."
                        }
                    )

                    print("\nAUTOMATION PAUSED")
                    print("The browser remains open.")
                    print("Please resolve the issue manually.")

                    input(
                        "Press Enter after human intervention "
                        "to resume..."
                    )

                    resume_handoff(
                        "Human reviewed the browser and approved continuation."
                    )

                    print("AUTOMATION RESUMED\n")

                    logs["status"] = "resumed"

            checkpoint = artifact["checkpoint"]

            success_text = page.locator(
                checkpoint["selector"]
            ).inner_text()

            if checkpoint["contains"] not in success_text:
                raise RuntimeError(
                    "Checkpoint validation failed"
                )

            logs["status"] = "success"
            logs["output"] = {
                "confirmation_message": success_text
            }

            page.screenshot(
                path=str(
                    PROJECT_ROOT
                    / "evidence"
                    / "replay"
                    / "replay-success.png"
                ),
                full_page=True
            )

            print("REPLAY RESULT:", success_text)

        except Exception as error:
            logs["status"] = "failed"
            logs["error"] = (
                type(error).__name__ + ": " + str(error)
            )

            page.screenshot(
                path=str(
                    PROJECT_ROOT
                    / "evidence"
                    / "replay"
                    / "replay-failure.png"
                ),
                full_page=True
            )

            raise

        finally:
            LOG_PATH.write_text(
                json.dumps(logs, indent=2),
                encoding="utf-8"
            )

            browser.close()


if __name__ == "__main__":
    replay_workflow(
        username="demo@creditunion.test",
        password="demo123",
        account_number="987654321",
        amount=250
    )