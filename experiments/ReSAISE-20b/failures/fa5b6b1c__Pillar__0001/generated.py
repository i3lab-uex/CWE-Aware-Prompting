# -*- coding: utf-8 -*-

"""
Secure command authorization module.

This module defines a function `authorize_and_run_cmd` that validates user-supplied
commands against a predefined whitelist (`ALLOWED_COMMANDS`). The function is
intentionally conservative: it normalizes the input, uses a set for efficient
membership checks, and never executes any command.  It returns the validated
command string if it is permitted, otherwise `None`.

The implementation avoids common pitfalls such as:
- Using mutable default arguments.
- Executing commands directly (CWE‑120, CWE‑78).
- Relying on string containment checks that could be spoofed.
"""

from __future__ import annotations

import re
from typing import Optional, Set


# --------------------------------------------------------------------------- #
# Configuration:  Define the set of safe commands.
# --------------------------------------------------------------------------- #

# Example whitelist. In a real system this would be loaded from a
# configuration file or environment variable and never modified at runtime.
ALLOWED_COMMANDS: Set[str] = {
    "ls",
    "cat",
    "echo",
    "date",
    "uptime",
    # Add more trusted commands here
}


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _normalize_command(cmd: str) -> str:
    """
    Normalizes a command string to mitigate whitespace and case issues.

    Parameters
    ----------
    cmd : str
        The raw command string supplied by the user.

    Returns
    -------
    str
        A trimmed, lower‑cased command suitable for whitelist comparison.
    """
    # Strip leading/trailing whitespace and collapse internal spaces
    cmd = re.sub(r"\s+", " ", cmd.strip())
    # Convert to lower case – whitelist is defined in lower case
    return cmd.lower()


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def authorize_and_run_cmd(command: str) -> Optional[str]:
    """
    Validate a user-supplied command against a whitelist.

    Parameters
    ----------
    command : str
        The raw command string entered by the user.

    Returns
    -------
    Optional[str]
        The normalized command if it is in `ALLOWED_COMMANDS`; otherwise,
        ``None``.
    """
    if not isinstance(command, str):
        # Reject non-string inputs immediately
        return None

    normalized = _normalize_command(command)

    if normalized in ALLOWED_COMMANDS:
        # In a real system you would now safely execute the command,
        # e.g., using subprocess.run([...], check=True, shell=False).
        return normalized

    return None