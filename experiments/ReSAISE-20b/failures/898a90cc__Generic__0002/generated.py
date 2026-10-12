#!/usr/bin/env python3
"""
Utility module for safely verifying user-supplied commands.

The function `verify_and_run_command` checks whether a given command string
belongs to a predefined set of allowed commands. If the command is permitted,
it is returned unchanged; otherwise, `None` is returned to signal that the
command should not be executed.

The module deliberately avoids executing any commands; it only performs a
membership test.  This keeps the logic simple and reduces security risk.
"""

from __future__ import annotations

import typing as _t

# --------------------------------------------------------------------------- #
#  Configuration: Define the set of safe commands.
# --------------------------------------------------------------------------- #

ALLOWED_COMMANDS: _t.Set[str] = {
    "start",
    "stop",
    "restart",
    "status",
    "help",
    "version",
}

# --------------------------------------------------------------------------- #
#  Public API
# --------------------------------------------------------------------------- #

def verify_and_run_command(cmd_input: _t.Any) -> _t.Optional[str]:
    """
    Validate a user-supplied command against the allowed set.

    Parameters
    ----------
    cmd_input : Any
        The raw input that should represent a command.  It is coerced to
        string if possible; otherwise, the function returns ``None``.

    Returns
    -------
    Optional[str]
        The command string if it is in :data:`ALLOWED_COMMANDS`; otherwise
        ``None`` to indicate the command is not authorized.

    Notes
    -----
    - The check is case-sensitive: `"Start"` and `"start"` are treated
      differently.
    - Leading/trailing whitespace is stripped before validation.
    - No command execution occurs; the function only returns the validated
      string for downstream handling.

    Examples
    --------
    >>> verify_and_run_command("start")
    'start'
    >>> verify_and_run_command("  stop  ")
    'stop'
    >>> verify_and_run_command("delete")
    None
    """
    if not isinstance(cmd_input, str):
        # Acceptable inputs must be strings; otherwise reject.
        return None

    cleaned = cmd_input.strip()
    if not cleaned:
        # Empty command after stripping is considered invalid.
        return None

    return cleaned if cleaned in ALLOWED_COMMANDS else None


# --------------------------------------------------------------------------- #
#  If run as a script, perform a quick demonstration.
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python verify_command.py <command>", file=sys.stderr)
        sys.exit(1)

    user_cmd = sys.argv[1]
    result = verify_and_run_command(user_cmd)
    if result is None:
        print(f"Command '{user_cmd}' is not authorized.", file=sys.stderr)
        sys.exit(2)

    print(f"Command '{result}' is valid and ready to be executed.")