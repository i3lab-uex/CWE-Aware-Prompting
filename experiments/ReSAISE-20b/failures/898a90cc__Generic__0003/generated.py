# -*- coding: utf-8 -*-
"""
Utility to validate and (optionally) execute user‑supplied commands.

The module defines a single public function, :func:`verify_and_run_command`,
which checks whether the supplied command string is in a predefined set of
allowed commands.  If the command is authorized, it is returned unchanged;
otherwise ``None`` is returned.

The implementation deliberately avoids executing the command directly,
as that would introduce serious security risks.  Should execution be
required in a trusted environment, it should be performed by a separate,
explicitly‑trusted wrapper that calls this function first.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import shlex
from typing import Optional, Set

# --------------------------------------------------------------------------- #
# Configuration: define the set of commands that are considered safe.
# --------------------------------------------------------------------------- #

ALLOWED_COMMANDS: Set[str] = {
    "ls",
    "cat",
    "echo",
    "date",
    # Add more safe commands here as needed.
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def verify_and_run_command(cmd_input: str) -> Optional[str]:
    """
    Validate a user‑supplied command against the list of allowed commands.

    Parameters
    ----------
    cmd_input : str
        The raw command string provided by the user.

    Returns
    -------
    Optional[str]
        The original command string if it is authorized; otherwise ``None``.
    """
    # Trim surrounding whitespace and split into tokens using shell parsing rules
    try:
        tokens = shlex.split(cmd_input)
    except ValueError:
        # Malformed command string (e.g., unmatched quotes)
        return None

    if not tokens:
        # Empty command is considered invalid
        return None

    cmd_name = tokens[0]
    if cmd_name in ALLOWED_COMMANDS:
        return cmd_input.strip()
    else:
        return None

# --------------------------------------------------------------------------- #
# Example usage (uncomment for testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_commands = [
        "ls -la",
        "rm -rf /",          # forbidden
        "echo 'Hello, world!'",
        "",
        "   ",
        "cat /etc/passwd"
    ]

    for cmd in test_commands:
        result = verify_and_run_command(cmd)
        print(f"Input: {cmd!r} -> {'Authorized' if result else 'Rejected'}")