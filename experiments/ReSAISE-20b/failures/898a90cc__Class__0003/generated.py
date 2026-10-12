#!/usr/bin/env python3
"""
Safe command verification module.

The function `verify_and_run_command` checks whether a user-supplied command
is present in the pre‑defined set `ALLOWED_COMMANDS`.  If it is, the command
string is returned unchanged.  Otherwise `None` is returned.

The implementation avoids any form of string interpolation or command
concatenation that could lead to injection vulnerabilities (CWE‑74).
"""

from typing import Optional

# --------------------------------------------------------------------------- #
# Define the set of commands that are considered safe for execution.
# The set should contain exact command strings as they will be matched
# verbatim.  No wildcard or pattern matching is performed to keep the check
# simple and secure.
# --------------------------------------------------------------------------- #
ALLOWED_COMMANDS = {
    "list_users",
    "create_user",
    "delete_user",
    "update_profile",
    "logout",
}

# --------------------------------------------------------------------------- #
def verify_and_run_command(cmd_input: str) -> Optional[str]:
    """
    Verify that the supplied command is allowed and return it if so.

    Parameters
    ----------
    cmd_input : str
        The command string provided by the user.

    Returns
    -------
    Optional[str]
        The original command if it is in `ALLOWED_COMMANDS`; otherwise
        ``None``.
    """
    # Strip leading/trailing whitespace to avoid accidental mismatches.
    command = cmd_input.strip()

    # Check membership in the allowed set.  The check is case‑sensitive
    # to avoid accidental aliasing of commands.
    if command in ALLOWED_COMMANDS:
        return command
    else:
        # Command not authorized; return None.
        return None

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Simple demonstration / test harness
    import sys

    if len(sys.argv) != 2:
        print("Usage: python verify_command.py <command>")
        sys.exit(1)

    user_cmd = sys.argv[1]
    result = verify_and_run_command(user_cmd)
    if result is None:
        print(f"Command '{user_cmd}' is not authorized.")
    else:
        print(f"Command '{result}' is authorized and ready to run.")