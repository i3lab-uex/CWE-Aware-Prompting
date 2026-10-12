# check_and_run_command.py

"""
This module provides a single function, `check_and_run_command`, which verifies
that a user supplied command is part of a predefined whitelist (`ALLOWED_COMMANDS`).
If the command is valid, it is returned unchanged; otherwise `None` is returned.
The function does **not** execute the command, thus avoiding any potential
command‑injection vulnerabilities.

The whitelist is defined as a tuple of exact command strings.  The comparison
is performed using strict equality, so any leading/trailing whitespace or
substitutions will cause the command to be rejected.

CWE-74 (Injection) is mitigated by ensuring that no external input is ever
interpolated into a command string or shell call; the function only performs
a safe membership check.
"""

from __future__ import annotations

# Define a whitelist of allowed commands.  Add or remove commands as needed.
ALLOWED_COMMANDS = (
    "list_users",
    "show_status",
    "restart_service",
    "update_config",
)

def check_and_run_command(command_input: str) -> str | None:
    """
    Validate a user‑supplied command against the whitelist.

    Parameters
    ----------
    command_input : str
        The raw input string from the user, expected to be a single command name.

    Returns
    -------
    str | None
        The original command string if it is in `ALLOWED_COMMANDS`;
        otherwise ``None``.
    """
    # Strip leading/trailing whitespace to avoid accidental mismatches.
    cleaned = command_input.strip()

    if cleaned in ALLOWED_COMMANDS:
        return cleaned

    # If the command is not allowed, do nothing and signal invalid input.
    return None