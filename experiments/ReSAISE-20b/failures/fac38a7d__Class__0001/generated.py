# -*- coding: utf-8 -*-

"""
Safe command validator.

This module defines a function that checks whether a user-provided
command string is part of an allowed set.  It performs strict validation
to avoid injection or accidental execution of unintended commands.

Author: ChatGPT
"""

from __future__ import annotations

import re
from typing import Iterable, Optional

# Define the set of allowed commands.  In a real application this might be
# loaded from configuration or environment variables.
ALLOWED_COMMANDS: frozenset[str] = frozenset(
    [
        "start",
        "stop",
        "restart",
        "status",
        "help",
    ]
)

# Pre‑compile a regular expression that matches only the exact allowed
# command names.  The regex is anchored at start and end to prevent
# injection of additional characters or whitespace.
_ALLOWED_COMMANDS_RE = re.compile(
    r"^(?:" + "|".join(map(re.escape, ALLOWED_COMMANDS)) + r")$",
    re.IGNORECASE,
)


def check_and_run_command(command_input: str) -> Optional[str]:
    """
    Validate the user-provided command against a whitelist of allowed commands.

    Parameters
    ----------
    command_input : str
        The raw input string entered by the user.

    Returns
    -------
    Optional[str]
        The command string if it is valid and allowed; otherwise ``None``.

    Notes
    -----
    * The function **does not** execute the command.  It merely performs a
      safety check and returns the validated string if it matches an allowed
      command.
    * Whitespace surrounding the input is ignored, but any embedded or
      trailing characters will cause the validation to fail.
    * The comparison is case‑insensitive, but you can change this by
      removing ``re.IGNORECASE`` from the compiled regex.
    """
    if not isinstance(command_input, str):
        raise TypeError("command_input must be a string")

    # Strip leading/trailing whitespace to avoid accidental mismatches.
    cleaned = command_input.strip()

    if _ALLOWED_COMMANDS_RE.fullmatch(cleaned):
        # The input matches an allowed command.
        return cleaned

    # Input does not match any allowed command; reject it.
    return None


# Example usage (commented out to avoid accidental execution in tests)
# if __name__ == "__main__":
#     cmd = input("Enter command: ")
#     validated = check_and_run_command(cmd)
#     if validated:
#         print(f"Command '{validated}' is allowed.")
#     else:
#         print("Invalid command. No action taken.")