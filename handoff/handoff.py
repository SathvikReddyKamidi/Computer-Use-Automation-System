import json
from pathlib import Path
from datetime import datetime


HANDOFF_DIR = Path("handoff")
HANDOFF_DIR.mkdir(exist_ok=True)

HANDOFF_FILE = HANDOFF_DIR / "active_handoff.json"


def create_handoff(
    reason: str,
    current_step: str,
    context: dict | None = None
) -> dict:
    handoff = {
        "handoff_id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "status": "awaiting_human",
        "reason": reason,
        "current_step": current_step,
        "context": context or {},
        "instructions": [
            "Automation is paused.",
            "Review the current browser state.",
            "Resolve the issue manually.",
            "Record the action taken.",
            "Confirm that automation may resume."
        ],
        "human_action": None,
        "created_at": datetime.now().isoformat(),
        "resumed_at": None
    }

    HANDOFF_FILE.write_text(
        json.dumps(handoff, indent=2),
        encoding="utf-8"
    )

    print("HUMAN HANDOFF CREATED")
    print(json.dumps(handoff, indent=2))

    return handoff


def resume_handoff(human_action: str) -> dict:
    if not HANDOFF_FILE.exists():
        raise FileNotFoundError("No active handoff found.")

    handoff = json.loads(
        HANDOFF_FILE.read_text(encoding="utf-8")
    )

    if handoff["status"] != "awaiting_human":
        raise ValueError("Handoff is not awaiting human intervention.")

    handoff["status"] = "resume_requested"
    handoff["human_action"] = human_action
    handoff["resumed_at"] = datetime.now().isoformat()

    HANDOFF_FILE.write_text(
        json.dumps(handoff, indent=2),
        encoding="utf-8"
    )

    print("HUMAN HANDOFF RESUME REQUESTED")
    print(json.dumps(handoff, indent=2))

    return handoff


if __name__ == "__main__":
    create_handoff(
        reason="Demo intervention request",
        current_step="submit_transfer",
        context={
            "url": "http://127.0.0.1:8001/transfer",
            "message": "Automation requires human assistance."
        }
    )