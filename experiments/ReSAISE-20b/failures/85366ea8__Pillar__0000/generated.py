# -*- coding: utf-8 -*-
"""
Utility to validate user commands against a whitelist of allowed actions.

The module defines:
* ALLOWED_COMMANDS – an immutable set containing the only commands that may be executed.
* check_and_execute_command – validates a user‑supplied command and returns it if valid,
  otherwise returns None.

The function is intentionally simple to avoid CWE‑707 issues: it never parses or
interprets the command string; it only checks membership in a known safe set.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# 1. Whitelist of safe commands
# --------------------------------------------------------------------------- #

ALLOWED_COMMANDS = frozenset(
    {
        "START",
        "STOP",
        "RESTART",
        "STATUS",
        "HELP",
    }
)

# --------------------------------------------------------------------------- #
# 2. Command validation
# --------------------------------------------------------------------------- #

def check_and_execute_command(usr_cmd: str) -> str | None:
    """
    Validate a user‑supplied command against the whitelist.

    Parameters
    ----------
    usr_cmd : str
        The raw input string provided by the user.

    Returns
    -------
    str | None
        The original command string if it is present in :data:`ALLOWED_COMMANDS`;
        otherwise ``None``.

    Notes
    -----
    * The comparison is case‑sensitive.  If you need a case‑insensitive
      check, convert the input to upper/lower case before calling this function.
    * The function performs **no** execution of the command; it merely signals
      whether the command is permitted.  Actual execution logic should be
      implemented elsewhere, using this function as a gatekeeper.
    """
    # Basic sanity checks: ensure the input is a string
    if not isinstance(usr_cmd, str):
        return None

    # Trim surrounding whitespace to avoid accidental mismatches
    cmd = usr_cmd.strip()

    # Return the command if it is in the whitelist, else None
    return cmd if cmd in ALLOWED_COMMANDS else None

# --------------------------------------------------------------------------- #
# Example usage (uncomment for quick test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_commands = [" START ", "invalid", "STOP", 123]
    for cmd in test_commands:
        result = check_and_execute_command(cmd)
        print(f"Input: {cmd!r} -> Result: {result!r}")