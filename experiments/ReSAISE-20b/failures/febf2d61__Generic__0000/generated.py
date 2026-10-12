# -*- coding: utf-8 -*-
"""
Safe command verifier.

This module defines a helper function `verify_and_run_command` that checks whether
a user-provided command string is part of a whitelist (`ALLOWED_COMMANDS`).
If the command is allowed, it is returned unchanged; otherwise `None` is
returned.  No execution of the command occurs within this function – the caller
must handle actual execution after verification.

The whitelist is stored as a `set` for efficient membership testing.
"""

from __future__ import annotations

# Define the set of allowed commands.  In a real application this list should
# contain only safe, non‑privileged operations.
ALLOWED_COMMANDS = {
    "list_files",
    "show_status",
    "restart_service",
    "update_config",
    "backup_data",
}

def verify_and_run_command(command: str) -> str | None:
    """
    Validate a user-provided command against the whitelist.

    Parameters
    ----------
    command : str
        The raw command string supplied by the user. Leading/trailing whitespace
        is ignored.

    Returns
    -------
    str | None
        The command string if it is in `ALLOWED_COMMANDS`; otherwise ``None``.

    Notes
    -----
    * The function performs a case‑sensitive match.  If you require case
      insensitivity, normalise the string before passing it in.
    * No command execution is performed here.  The caller should handle
      executing the verified command.
    """
    # Normalise input: strip whitespace, but keep internal spaces if any
    cleaned = command.strip()

    # Quick membership test; set lookup is O(1)
    if cleaned in ALLOWED_COMMANDS:
        return cleaned

    # If not allowed, silently ignore
    return None


# Example usage (commented out; remove for production)
if __name__ == "__main__":
    test_commands = ["list_files", "delete_all", " restart_service ", ""]
    for cmd in test_commands:
        result = verify_and_run_command(cmd)
        print(f"Input: {cmd!r} -> Result: {result!r}")