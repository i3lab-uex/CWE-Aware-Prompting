#!/usr/bin/env python3
"""
Utility for authorizing user supplied commands.

The module defines a set of trusted commands and exposes the
function `authorize_and_run_cmd` which validates an input command
against this whitelist.  If the command is allowed, it is returned;
otherwise `None` is returned.

The implementation uses a set for O(1) lookup and performs basic
type and whitespace checks to guard against accidental injection or
malformed input.  No command is executed here; the caller may do so
after validating the result.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Configuration: define a set of commands considered safe.
# --------------------------------------------------------------------------- #

ALLOWED_COMMANDS = {
    "list",
    "show",
    "status",
    "restart",
    "shutdown",
    # Add more safe commands as required.
}

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def authorize_and_run_cmd(command: str) -> str | None:
    """
    Validate a user supplied command against the trusted list.

    Parameters
    ----------
    command : str
        The raw command string supplied by the user.

    Returns
    -------
    str | None
        The original command if it is in :data:`ALLOWED_COMMANDS`;
        otherwise ``None``.

    Notes
    -----
    - The function performs a strict membership test against the set
      :data:`ALLOWED_COMMANDS`.  No normalization beyond trimming
      leading/trailing whitespace is performed to avoid accidental
      aliasing or injection.
    - The caller must ensure that the returned command is executed in a
      safe context.  This function only authorizes, it does not run the
      command.
    """
    if not isinstance(command, str):
        # Non-string inputs are automatically rejected.
        return None

    # Trim whitespace to avoid accidental mismatches like " list ".
    cleaned = command.strip()

    if not cleaned:
        # Empty commands are rejected.
        return None

    if cleaned in ALLOWED_COMMANDS:
        return cleaned
    else:
        return None

# --------------------------------------------------------------------------- #
# Example usage (for manual testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_commands = ["list", "  status ", "unknown", "", None]
    for cmd in test_commands:
        result = authorize_and_run_cmd(cmd if isinstance(cmd, str) else "")
        print(f"Input: {repr(cmd):>10} -> Authorized: {result!r}")