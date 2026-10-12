#!/usr/bin/env python3
"""
Safe command validator.

The module defines a single function, `check_and_run_command`, which ensures that
any user‑supplied command is part of a predefined whitelist before it can be
executed.  This protects against command‑injection attacks (CWE‑74) by refusing
to run arbitrary or malicious input.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Configuration: list of commands that are considered safe.
# --------------------------------------------------------------------------- #

ALLOWED_COMMANDS = {
    "list_files",
    "show_disk_usage",
    "check_health",
    # Add other safe commands here
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def check_and_run_command(command: str) -> str | None:
    """
    Validate a user‑supplied command against the whitelist.

    Parameters
    ----------
    command : str
        The command string supplied by a user or external source.

    Returns
    -------
    str | None
        The original command if it is authorized; otherwise, ``None``.
    """
    # Defensive copy and normalise the input to avoid accidental modifications
    if not isinstance(command, str):
        return None

    cleaned_command = command.strip()

    # Fast membership test in the immutable set
    if cleaned_command in ALLOWED_COMMANDS:
        return cleaned_command

    # Reject everything else
    return None


# --------------------------------------------------------------------------- #
# Example usage (for demonstration only; remove or guard under `if __name__ == "__main__":` in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Simulate user input
    test_commands = [
        "list_files",
        "rm -rf /",          # malicious
        "   show_disk_usage ",
        "unknown_command"
    ]

    for cmd in test_commands:
        result = check_and_run_command(cmd)
        if result is None:
            print(f"Command '{cmd}' rejected: not authorized.")
        else:
            print(f"Command '{result}' accepted and ready for execution.")