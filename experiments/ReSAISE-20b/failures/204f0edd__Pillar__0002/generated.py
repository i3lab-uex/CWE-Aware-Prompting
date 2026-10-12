#!/usr/bin/env python3
"""
Utility to validate user-supplied commands against a whitelist.

The function `check_and_run_command` returns the command if it is present
in the global set `ALLOWED_COMMANDS`.  If the command is not authorized,
`None` is returned.  No execution of the command occurs here; this module
is solely responsible for validation, which helps prevent injection or
other misuse.

CWE-707 (Improper Neutralization of Structured Data) is mitigated by
strictly checking the command string against an explicit set of allowed
values, ensuring that only well‑formed, known commands are accepted.
"""

from typing import Optional

# Example whitelist.  Replace or extend this set with the real allowed commands.
ALLOWED_COMMANDS = {
    "start",
    "stop",
    "restart",
    "status",
    "reload-config",
}

def check_and_run_command(command: str) -> Optional[str]:
    """
    Validate a user-supplied command against the whitelist.

    Parameters
    ----------
    command : str
        The raw command string supplied by a user or external source.

    Returns
    -------
    Optional[str]
        The command string if it is present in ALLOWED_COMMANDS; otherwise
        None.

    Notes
    -----
    * The comparison is case‑sensitive and exact; no trimming or normalization
      occurs.  If you need case‑insensitivity, adjust the whitelist accordingly.
    * No command execution is performed here; this function merely validates
      that the command is authorized.
    """
    # Ensure the input is a string; otherwise reject immediately.
    if not isinstance(command, str):
        return None

    # Direct membership test against the whitelist.
    if command in ALLOWED_COMMANDS:
        return command

    # Command not authorized
    return None