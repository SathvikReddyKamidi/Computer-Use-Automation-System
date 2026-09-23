import json
from urllib.parse import urlparse


BLOCKED_ACTIONS = {
    "delete",
    "withdraw",
    "close_account",
    "external_navigation",
}


def validate_artifact(artifact: dict) -> tuple[bool, list[str]]:
    errors = []

    target = artifact.get("target", {})
    base_url = target.get("base_url", "")
    allowed_routes = set(target.get("allowed_routes", []))

    if not base_url:
        errors.append("Missing target base_url")

    for step in artifact.get("steps", []):
        action = step.get("action")
        step_id = step.get("step_id", "unknown")

        if action in BLOCKED_ACTIONS:
            errors.append(
                f"Step '{step_id}' uses blocked action '{action}'"
            )

        if action == "navigate":
            route = step.get("url", "")

            if route not in allowed_routes:
                errors.append(
                    f"Step '{step_id}' navigates to unauthorized route '{route}'"
                )

            if route.startswith("http"):
                parsed_base = urlparse(base_url)
                parsed_route = urlparse(route)

                if parsed_route.netloc != parsed_base.netloc:
                    errors.append(
                        f"Step '{step_id}' attempts external navigation"
                    )

    safety = artifact.get("safety", {})

    if safety.get("secrets_in_artifact", True):
        errors.append("Artifact must not contain secrets")

    if safety.get("raw_pii_in_logs", True):
        errors.append("Raw PII logging must be disabled")

    return len(errors) == 0, errors


if __name__ == "__main__":
    with open(
        "artifacts/transfer_workflow.json",
        "r",
        encoding="utf-8"
    ) as file:
        artifact = json.load(file)

    valid, errors = validate_artifact(artifact)

    if valid:
        print("SAFETY VALIDATION: PASSED")
    else:
        print("SAFETY VALIDATION: FAILED")
        for error in errors:
            print("-", error)
