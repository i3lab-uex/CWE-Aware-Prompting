#!/usr/bin/env python3
"""
A minimal, secure command validator.

The module defines a set of allowed commands and provides the
`check_and_execute_command()` function that verifies whether a user-
supplied command is permitted.  If the command is allowed, it is
returned unchanged (the caller may decide how to execute it).  If
not, `None` is returned.

Security notes:
- The function performs strict string matching against a predefined
  set of commands; no shell injection is possible.
- It normalises the input by stripping leading/trailing whitespace
  and rejecting empty strings or non‑string values.
- No external data is parsed or executed, mitigating CWE‑707
  (Improper Neutralization of Structured Data).
"""

from __future__ import annotations

import subprocess
from typing import Optional, Set

# ----------------------------------------------------------------------
# Configuration: define which commands are safe to run.
# ----------------------------------------------------------------------
ALLOWED_COMMANDS: Set[str] = {
    "list",
    "status",
    "restart",
}

# ----------------------------------------------------------------------
# Core functionality
# ----------------------------------------------------------------------


def check_and_execute_command(usr_cmd: str) -> Optional[str]:
    """
    Validate a user‑supplied command against the allowed set.

    Parameters
    ----------
    usr_cmd : str
        The raw user input intended to be executed.

    Returns
    -------
    Optional[str]
        The command string if it is allowed; otherwise ``None``.

    Notes
    -----
    * Only exact matches (case‑sensitive) are accepted.
    * Leading/trailing whitespace is ignored.
    * No attempt to parse arguments or shell metacharacters is made;
      this keeps the function free from injection risks.
    """
    # Basic type check
    if not isinstance(usr_cmd, str):
        return None

    # Normalise input: strip whitespace
    cmd = usr_cmd.strip()
    if not cmd:
        return None

    # Strict membership test
    if cmd in ALLOWED_COMMANDS:
        # Example execution (commented out to avoid side effects).
        #
        # In a real application you would probably want to run the
        # command via subprocess with shell=False, e.g.:
        #
        #     subprocess.run([cmd], check=True)
        #
        # For this exercise we simply return the command string.
        return cmd

    return None


# ----------------------------------------------------------------------
# Example usage (disabled by default)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python check_and_execute_command.py <command>")
        sys.exit(1)

    user_input = sys.argv[1]
    validated_cmd = check_and_execute_command(user_input)
    if validated_cmd is None:
        print(f"Command '{user_input}' is not allowed.")
    else:
        print(f"Executing safe command: {validated_cmd}")
        # Uncomment the line below to actually run the command.
        # subprocess.run([validated_cmd], check=True)