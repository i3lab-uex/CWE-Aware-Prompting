# -*- coding: utf-8 -*-

"""
A simple command validator that ensures a user supplied command is part of an
explicitly allowed set before it can be executed or returned.

The module defines:
    - ALLOWED_COMMANDS: a frozenset containing the commands that are considered safe.
    - validate_and_run_cmd(usr_command): validates and returns the command if allowed,
      otherwise returns None.

Security notes:
    * Commands are compared in a case‑sensitive manner. If you need case‑insensitivity,
      normalise the input before comparison.
    * The function does not execute any command; it only validates and returns the
      string. Execution must be handled by a separate, audited routine.
    * By using a frozenset for ALLOWED_COMMANDS we prevent accidental modification
      of the allowed list at runtime, mitigating potential CWE-707 style issues.
"""

from __future__ import annotations

# Define the set of commands that are considered safe.
ALLOWED_COMMANDS = frozenset({
    "ls",
    "cat",
    "grep",
    "pwd",
    "echo",
    "date",
})

def validate_and_run_cmd(usr_command: str) -> str | None:
    """
    Validate that the supplied user command is part of the allowed list.

    Parameters
    ----------
    usr_command : str
        The command string entered by the user.

    Returns
    -------
    str | None
        The original command if it is allowed; otherwise, None.
    """
    # Basic sanitisation: strip surrounding whitespace
    cmd = usr_command.strip()

    # Quick exit for empty strings
    if not cmd:
        return None

    # Validate against the allowed command set
    if cmd in ALLOWED_COMMANDS:
        return cmd

    # If the command is not allowed, do not expose any details
    return None