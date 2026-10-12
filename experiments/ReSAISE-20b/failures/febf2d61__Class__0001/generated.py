# verify_and_run_command.py

"""
This module provides a safe command verification helper.
It checks whether the supplied user command is in a predefined
whitelist of allowed commands and returns it if valid.
No execution is performed to avoid injection risks.

CWE-74 Mitigation:
  - The function never interpolates or executes the command.
  - It performs a strict membership test against an immutable set,
    ensuring that only explicitly permitted commands are accepted.
"""

from __future__ import annotations

# ----------------------------------------------------------------------
# Whitelist of safe, user‑permitted commands.
# Add or remove entries as required for your application.
# ----------------------------------------------------------------------
ALLOWED_COMMANDS = {
    "list_files",
    "show_date",
    "display_status",
    # Add more safe commands here
}

def verify_and_run_command(command: str) -> str | None:
    """
    Validate a user‑supplied command against the ALLOWED_COMMANDS set.

    Parameters
    ----------
    command : str
        The raw user input intended to be a command.

    Returns
    -------
    str | None
        The original command string if it is in the whitelist,
        otherwise ``None``.
    """
    # Strip surrounding whitespace to avoid accidental mismatches
    sanitized = command.strip()

    # Fast membership check in an immutable set (O(1) average)
    if sanitized in ALLOWED_COMMANDS:
        return sanitized
    return None

# ----------------------------------------------------------------------
# Example usage (for illustration only; remove or guard with `if __name__ == "__main__":` in production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Simulate user input
    user_input = "list_files"
    result = verify_and_run_command(user_input)
    if result is not None:
        print(f"Command '{result}' approved.")
    else:
        print("Invalid command received; ignoring.")