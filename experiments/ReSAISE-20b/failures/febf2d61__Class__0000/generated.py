# verify_and_run_command.py

from typing import Optional, List

# Predefined list of commands that are allowed to be executed
ALLOWED_COMMANDS: List[str] = [
    "list_users",
    "create_user",
    "delete_user",
    "update_profile",
    "logout"
]

def verify_and_run_command(command: str) -> Optional[str]:
    """
    Validate a user-issued command against the allowed commands list.

    Args:
        command: The raw command string supplied by the user.

    Returns:
        The validated command string if it is in ALLOWED_COMMANDS,
        otherwise None.

    Notes:
        - The function performs a strict membership test; no string
          manipulation or pattern matching is used, which mitigates the risk
          of injection (CWE‑74).
        - The function does not execute the command; it merely validates
          and returns it. Execution logic should be handled elsewhere.
    """
    # Normalize whitespace to avoid accidental mismatches
    normalized = command.strip()

    # Quick check for empty input
    if not normalized:
        return None

    # Use a set for O(1) membership testing
    allowed_set = set(ALLOWED_COMMANDS)

    if normalized in allowed_set:
        return normalized

    # Command is not permitted
    return None