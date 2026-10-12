# -*- coding: utf-8 -*-
"""
Utility to validate user‑supplied commands against a whitelist.
This module intentionally avoids executing the command; it only
returns the string if it is present in ALLOWED_COMMANDS.
"""

import re
from typing import Optional

# A minimal example of allowed commands. In a real system this would be
# populated from configuration or environment variables.
ALLOWED_COMMANDS = {
    "ls -la",
    "git status",
    "docker ps",
    "python --version",
}

def _canonicalize(cmd: str) -> str:
    """
    Normalise a command string for comparison.

    * Strip leading/trailing whitespace.
    * Collapse internal runs of whitespace to a single space.
    * Preserve case (commands are typically case‑sensitive).
    """
    # Remove leading/trailing whitespace
    cmd = cmd.strip()
    # Collapse internal whitespace (tabs, newlines, multiple spaces)
    cmd = re.sub(r"\s+", " ", cmd)
    return cmd

def verify_and_run_command(cmd_input: str) -> Optional[str]:
    """
    Validate a user‑supplied command against the whitelist.

    Parameters
    ----------
    cmd_input : str
        The raw command string supplied by the user.

    Returns
    -------
    Optional[str]
        The canonicalised command if it is in ALLOWED_COMMANDS;
        otherwise None.

    Notes
    -----
    * No command execution is performed.
    * The function is deliberately defensive: it normalises the input
      and performs an exact set membership test.
    * The implementation is resistant to CWE‑707 by ensuring that the
      command string is strictly validated before any downstream use.
    """
    canonical_cmd = _canonicalize(cmd_input)

    if canonical_cmd in ALLOWED_COMMANDS:
        return canonical_cmd

    # Command is not authorized
    return None