import json
from pathlib import Path

from core.safety import validate_artifact


def test_artifact_exists():
    path = Path("artifacts/transfer_workflow.json")
    assert path.exists()


def test_artifact_is_valid():
    with open(
        "artifacts/transfer_workflow.json",
        "r",
        encoding="utf-8"
    ) as file:
        artifact = json.load(file)

    valid, errors = validate_artifact(artifact)

    assert valid, errors


def test_handoff_exists():
    path = Path("handoff/active_handoff.json")
    assert path.exists()


def test_replay_log_exists():
    path = Path("evidence/replay/replay_log.json")
    assert path.exists()
