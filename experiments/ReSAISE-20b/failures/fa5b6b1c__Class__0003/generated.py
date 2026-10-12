#!/usr/bin/env python3
"""
Secure command authorisation module.

This module exposes a single function, `authorize_and_run_cmd`, which checks whether
a user-provided command is part of a pre‑defined whitelist (`ALLOWED_COMMANDS`).
If the command is authorised, it is returned unchanged; otherwise `None` is
returned.  No command execution or string interpolation occurs within this module,
preventing injection vulnerabilities (CWE‑74).

Author: OpenAI ChatGPT
"""

from typing import Optional, Set

# Define a whitelist of safe commands.
ALLOWED_COMMANDS: Set[str] = {
    "list",
    "status",
    "restart",
    "shutdown",
    "help",
}

def authorize_and_run_cmd(command: str) -> Optional[str]:
    """
    Validate a user‑supplied command against the allowed list.

    Parameters
    ----------
    command : str
        The raw command string provided by the user.  Leading/trailing whitespace is ignored.

    Returns
    -------
    Optional[str]
        The command string if it is in the whitelist; otherwise None.

    Notes
    -----
    - The comparison is case‑sensitive and exact.
    - No attempt is made to execute the command here; this function only performs
      authorisation.  Execution should be handled by a separate, well‑sanitised module.
    """
    # Normalise input: strip whitespace but keep case for strict matching
    cleaned = command.strip()
    if cleaned in ALLOWED_COMMANDS:
        return cleaned
    return None