# verify_and_run_command.py

"""
This module provides a safe command verification function.
It ensures that only commands from the predefined ALLOWED_COMMANDS
set are accepted, mitigating command injection risks (CWE-707).
"""

from __future__ import annotations

# Define the set of commands that are permitted.
ALLOWED_COMMANDS = {
    "list",          # e.g., list files
    "status",        # show status
    "restart",       # restart service
    "shutdown",      # shutdown system
    "help",          # display help
}

def verify_and_run_command(command: str) -> str | None:
    """
    Validate a user-provided command against the ALLOWED_COMMANDS set.

    Parameters
    ----------
    command : str
        The raw user input command string.

    Returns
    -------
    str | None
        The original command if it is allowed; otherwise, None.

    Notes
    -----
    - Leading/trailing whitespace is stripped before validation.
    - The check is case-sensitive; adjust as needed for your context.
    - This function does *not* execute the command – it merely verifies
      its validity. Execution should be handled elsewhere with strict
      controls.
    """
    # Normalize the input: strip whitespace, keep case as-is.
    cleaned_command = command.strip()

    # Quick exit if the command is empty after stripping.
    if not cleaned_command:
        return None

    # Check against the allowed set.
    if cleaned_command in ALLOWED_COMMANDS:
        return cleaned_command

    # If not allowed, return None.
    return None