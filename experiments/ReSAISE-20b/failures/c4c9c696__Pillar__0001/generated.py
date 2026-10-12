#!/usr/bin/env python3
"""
Secure command validator.

The function `check_and_run_command` ensures that a user-provided command
is part of an explicit whitelist (`ALLOWED_COMMANDS`).  Only commands that
exactly match one of the allowed entries are accepted; all others result
in `None`.  The implementation normalises whitespace and enforces a
strict comparison to avoid accidental acceptance of malicious input.

Author: ChatGPT
"""

from typing import Optional, Iterable

# --------------------------------------------------------------------------- #
# Configuration: define the set of commands that are considered safe.
# --------------------------------------------------------------------------- #

ALLOWED_COMMANDS: Iterable[str] = (
    "list",
    "show",
    "delete",
    "create",
    "update",
)

# Convert to a set for O(1) lookups.
_ALLOWED_COMMANDS_SET = {cmd.strip() for cmd in ALLOWED_COMMANDS}


def check_and_run_command(user_input: str) -> Optional[str]:
    """
    Validate a user-provided command against a whitelist.

    Parameters
    ----------
    user_input : str
        Raw input string from the user, potentially containing leading/trailing
        whitespace or newline characters.

    Returns
    -------
    Optional[str]
        The normalised command string if it is present in the whitelist;
        otherwise, `None`.

    Notes
    -----
    - The comparison is case-sensitive; if you wish to allow a case-insensitive
      match, adjust the set and comparison accordingly.
    - No side effects are performed; this function merely validates the
      command.  Execution of the command should be handled elsewhere.
    """
    # Strip leading/trailing whitespace to avoid accidental mismatches.
    command = user_input.strip()

    if command in _ALLOWED_COMMANDS_SET:
        return command

    # Command not allowed; do not execute.
    return None