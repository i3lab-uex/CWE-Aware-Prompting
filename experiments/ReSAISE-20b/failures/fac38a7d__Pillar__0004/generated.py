# -*- coding: utf-8 -*-
"""
Secure command validation module.

This module defines a single function, `check_and_run_command`, which verifies
whether a user-provided command string is within an allowed set of commands.
If the command is valid, it returns the original string; otherwise, it
returns None. No execution of external commands occurs in this function,
ensuring protection against command injection attacks.

CWE-707: The function ensures that only well‑formed, predefined commands
are accepted before any downstream processing.
"""

from typing import Optional

# Define the set of allowed commands. Adjust this list as needed for your
# application context. Using a frozenset makes the set immutable and hashable,
# which can help avoid accidental modifications.
ALLOWED_COMMANDS = frozenset({
    "list",
    "show",
    "delete",
    "create",
    "update",
    # Add additional safe commands here.
})


def check_and_run_command(command_input: str) -> Optional[str]:
    """
    Validate the user-provided command against a predefined set of safe commands.

    Parameters
    ----------
    command_input : str
        The raw input string from the user. Leading/trailing whitespace is ignored.

    Returns
    -------
    Optional[str]
        The original command string if it matches an allowed command;
        otherwise, None.

    Notes
    -----
    - The comparison is case-sensitive; adjust the logic if a case‑insensitive
      check is required.
    - This function does not execute the command. It merely performs validation,
      delegating execution to a separate, properly secured routine.
    """
    # Normalise input: strip whitespace but preserve the original string for
    # potential debugging or logging purposes.
    trimmed = command_input.strip()

    if trimmed in ALLOWED_COMMANDS:
        return trimmed
    else:
        return None