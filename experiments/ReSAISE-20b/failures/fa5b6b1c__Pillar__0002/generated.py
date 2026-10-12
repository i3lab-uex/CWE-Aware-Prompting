# SPDX-License-Identifier: MIT
"""
Command authorization module.

This module defines a set of trusted commands and provides a helper
function to validate user input against that list.  The function is
intentionally conservative: it requires an exact match (including case)
and does not perform any further processing on the command string.
"""

# Trusted commands – keep this list short and well‑documented.
ALLOWED_COMMANDS = {
    "list_files",
    "show_status",
    "restart_service",
    "shutdown_system",
}

def authorize_and_run_cmd(command: str) -> str | None:
    """
    Validate a user‑supplied command against the trusted list.

    Parameters
    ----------
    command : str
        The raw command string supplied by the user.

    Returns
    -------
    str | None
        The original command if it is in ALLOWED_COMMANDS, otherwise None.

    Notes
    -----
    - The comparison is case‑sensitive and requires an exact match.
    - No command execution occurs in this function; it merely authorizes.
    """
    # Strip surrounding whitespace to avoid accidental mismatches.
    cleaned = command.strip()

    if cleaned in ALLOWED_COMMANDS:
        return cleaned
    return None