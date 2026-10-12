#!/usr/bin/env python3
"""
Safe command validation module.

This module defines `check_and_execute_command`, which checks a user‑supplied
command string against a predefined whitelist of allowed commands.  If the
command is permitted, it is returned unchanged; otherwise `None` is
returned.  The function deliberately does **not** execute the command,
avoiding CWE‑74 injection risks.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# 1. Define the whitelist of allowed commands
# --------------------------------------------------------------------------- #

ALLOWED_COMMANDS = {
    "list",      # e.g., list directory contents
    "status",    # e.g., show system status
    "help",      # provide help information
    "exit",      # terminate the session
}

# --------------------------------------------------------------------------- #
# 2. Command validation function
# --------------------------------------------------------------------------- #

def check_and_execute_command(usr_cmd: str) -> str | None:
    """
    Validate a user‑supplied command against the allowed commands whitelist.

    Parameters
    ----------
    usr_cmd : str
        The raw command string entered by the user.

    Returns
    -------
    str | None
        The original command if it is allowed; otherwise `None`.

    Notes
    -----
    * Leading/trailing whitespace is ignored.
    * The comparison is case‑sensitive; modify `ALLOWED_COMMANDS` if
      case‑insensitivity is desired.
    * This function does **not** execute the command; it merely validates
      and returns it for downstream execution if desired.
    """
    # Strip whitespace to avoid accidental mismatches
    cleaned_cmd = usr_cmd.strip()

    # Quick exit for empty input
    if not cleaned_cmd:
        return None

    # Validate against the whitelist
    if cleaned_cmd in ALLOWED_COMMANDS:
        return cleaned_cmd

    # Command not allowed
    return None


# --------------------------------------------------------------------------- #
# 3. Example usage (for demonstration; remove in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python safe_cmd.py <command>")
        sys.exit(1)

    user_input = sys.argv[1]
    result = check_and_execute_command(user_input)

    if result is None:
        print(f"Command '{user_input}' is not allowed.")
    else:
        print(f"Command '{result}' validated and ready for execution.")