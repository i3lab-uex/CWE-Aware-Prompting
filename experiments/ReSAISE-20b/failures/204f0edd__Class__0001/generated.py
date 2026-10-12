# -*- coding: utf-8 -*-
"""
Safe command validation module.

This module defines a single public function `check_and_run_command` that
verifies whether a user‑supplied command is present in the predefined set of
allowed commands.  The function performs strict equality comparison and
normalises whitespace to guard against injection attacks (CWE‑74).

Author: OpenAI ChatGPT
"""

import re
from typing import Optional

# --------------------------------------------------------------------------- #
# 1. Allowed commands set (example)
# --------------------------------------------------------------------------- #

ALLOWED_COMMANDS = {
    "LIST_FILES",
    "REMOVE_FILE",
    "COPY_FILE",
    "MOVE_FILE",
    # Add additional safe commands here
}

# --------------------------------------------------------------------------- #
# 2. Helper utilities
# --------------------------------------------------------------------------- #

# Regular expression that matches a valid command name: uppercase letters, digits,
# and underscores only. This prevents shell metacharacters or whitespace
# injection.
_VALID_COMMAND_RE = re.compile(r"^[A-Z0-9_]+$")

def _is_valid_command(cmd: str) -> bool:
    """
    Internal helper that checks if the command string contains only allowed
    characters.  It also strips leading/trailing whitespace to avoid
    accidental mismatches.
    """
    stripped = cmd.strip()
    return bool(_VALID_COMMAND_RE.fullmatch(stripped))

# --------------------------------------------------------------------------- #
# 3. Public API
# --------------------------------------------------------------------------- #

def check_and_run_command(command: str) -> Optional[str]:
    """
    Validate the supplied command against a whitelist of safe commands.

    Parameters
    ----------
    command : str
        The user‑supplied command string. It may contain leading/trailing
        whitespace.

    Returns
    -------
    Optional[str]
        The stripped command string if it is present in :data:`ALLOWED_COMMANDS`;
        otherwise ``None`` indicating an unauthorized command.

    Notes
    -----
    * The function performs strict equality comparison; no partial matches are
      allowed.
    * Whitespace is trimmed before validation to make the comparison robust
      against accidental spaces or newlines.
    * A regular expression check ensures that the command contains only
      characters allowed in the whitelist, mitigating injection attacks.
    """
    # Strip whitespace to avoid accidental mismatches
    cleaned = command.strip()

    # Quick sanity check: only allowed characters
    if not _is_valid_command(cleaned):
        return None

    # Strict whitelist check
    if cleaned in ALLOWED_COMMANDS:
        return cleaned

    return None

# --------------------------------------------------------------------------- #
# 4. Example usage (for testing purposes only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_commands = [
        "  LIST_FILES ",
        "REMOVE_FILE",
        "UNSAFE_COMMAND",
        "COPY_FILE; rm -rf /",  # injection attempt
    ]

    for cmd in test_commands:
        result = check_and_run_command(cmd)
        print(f"Input: {cmd!r} -> Result: {result}")