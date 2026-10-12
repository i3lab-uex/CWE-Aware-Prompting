# -*- coding: utf-8 -*-
"""
Utility to validate user supplied commands against a whitelist.

The module defines a small, immutable set of allowed commands.  The
`validate_and_run_cmd()` function checks if a user supplied command is
present in that set.  If it is, the command string is returned; otherwise,
`None` is returned.

This implementation avoids mutable global state, uses a frozenset for
immunity to accidental modification, and performs a fast membership test.
"""

from __future__ import annotations

# Define the set of commands that are considered safe to run.
ALLOWED_COMMANDS: frozenset[str] = frozenset(
    {
        "start",
        "stop",
        "restart",
        "status",
        "help",
    }
)


def validate_and_run_cmd(usr_command: str) -> str | None:
    """
    Validate a user supplied command against the whitelist.

    Parameters
    ----------
    usr_command : str
        The command string supplied by a user.  It may contain leading or
        trailing whitespace; this function normalises it.

    Returns
    -------
    str | None
        The trimmed command if it is in `ALLOWED_COMMANDS`; otherwise,
        `None`.

    Notes
    -----
    - The function performs a case‑sensitive comparison.
    - Leading/trailing whitespace is stripped before validation.
    - No side effects or execution of the command occur here; the caller
      can decide what to do with the validated command.
    """
    # Normalise whitespace: strip leading/trailing spaces.
    cmd = usr_command.strip()

    if cmd in ALLOWED_COMMANDS:
        return cmd
    return None


# Example usage (commented out – remove for production)
if __name__ == "__main__":
    test_commands = ["start", "  stop  ", "invalid", "help"]
    for cmd in test_commands:
        result = validate_and_run_cmd(cmd)
        print(f"Input: {cmd!r} → Validated: {result!r}")