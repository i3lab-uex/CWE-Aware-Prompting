#!/usr/bin/env python3
"""
Utility to validate a user supplied command against a whitelist of safe commands.
"""

from __future__ import annotations

import re
from typing import Optional, Set

# A minimal set of allowed commands. Extend this list as needed.
ALLOWED_COMMANDS: Set[str] = {
    "list",
    "show",
    "help",
    "exit",
    "quit",
}

# Regular expression to match a single word command (no spaces or special chars).
_COMMAND_RE = re.compile(r"^\w+$")


def validate_and_run_cmd(usr_command: str) -> Optional[str]:
    """
    Validate that the user supplied command is in the ALLOWED_COMMANDS set.

    Parameters
    ----------
    usr_command : str
        The raw command string entered by the user.

    Returns
    -------
    Optional[str]
        The cleaned command if it is allowed; otherwise, None.

    Notes
    -----
    * Leading and trailing whitespace are stripped.
    * The command is matched case‑insensitively.
    * A simple word check prevents accidental injection of shell meta characters.
    """
    # Strip whitespace
    cmd = usr_command.strip()

    # Ensure the command is a single word (no spaces or special characters)
    if not _COMMAND_RE.match(cmd):
        return None

    # Case‑insensitive comparison against the whitelist
    if cmd.lower() in (c.lower() for c in ALLOWED_COMMANDS):
        return cmd
    return None


# Example usage (remove or guard with if __name__ == "__main__": in real code)
if __name__ == "__main__":
    test_commands = ["list", "  help ", "rm -rf /", "exit"]
    for cmd in test_commands:
        result = validate_and_run_cmd(cmd)
        print(f"Input: {cmd!r} -> Output: {result!r}")