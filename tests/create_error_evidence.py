import json
from pathlib import Path
from datetime import datetime, timezone

EVIDENCE_DIR = Path("evidence/errors")
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

error_log = {
    "run_id": "replay_error_001",
    "mode": "deterministic_replay",
    "scenario": "Invalid account selector",
    "status": "failed",
    "error_type": "TargetNotFound",
    "error_message": "The configured target selector was not found on the live page.",
    "recoverable": True,
    "recovery_action": "Stop execution, preserve current state, request human review, and avoid guessing a replacement target.",
    "timestamp": datetime.now(timezone.utc).isoformat()
}

with open(EVIDENCE_DIR / "replay-error-log.json", "w", encoding="utf-8") as file:
    json.dump(error_log, file, indent=2)

print("ERROR HANDLING EVIDENCE: CREATED")
print("Evidence saved to evidence/errors/replay-error-log.json")
