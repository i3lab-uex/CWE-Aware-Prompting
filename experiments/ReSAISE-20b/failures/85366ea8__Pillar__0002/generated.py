#!/usr/bin/env python3
"""
A small helper that validates user‑supplied commands against a whitelist of allowed
commands.  The function does **not** execute the command; it simply returns the
command string if it is permitted, or `None` otherwise.

The implementation avoids common pitfalls such as accidental whitespace
inclusion, case‑sensitive mismatches, or accidental execution of arbitrary
input.  It also uses a `set` for O(1) lookup time and normalises the input
before comparison.

CWE‑707 (Improper Neutralization) is mitigated by ensuring that the command
string returned has been explicitly checked against a trusted set of values.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Configuration:  Define the whitelist of commands that are considered safe.
# The list can be extended as needed, but each entry should be a *literal*
# string that represents the exact command you wish to allow.
# --------------------------------------------------------------------------- #
ALLOWED_COMMANDS = {
    "list_files",
    "show_date",
    "ping_google",
    "backup_db",
    # Add more safe commands here...
}

def check_and_execute_command(usr_cmd: str) -> str | None:
    """
    Validate a user‑supplied command against the whitelist.

    Parameters
    ----------
    usr_cmd : str
        The raw command string supplied by the user.

    Returns
    -------
    str | None
        The original command string if it is in `ALLOWED_COMMANDS`;
        otherwise, `None`.

    Notes
    -----
    * The comparison is case‑sensitive; if you want to allow case‑insensitive
      matching, convert both the input and the whitelist entries to a common
      case (e.g., lower()).
    * Leading/trailing whitespace is stripped before the lookup to avoid
      accidental mismatches caused by accidental spaces.
    * The function deliberately **does not** execute the command.  Execution
      should be handled by a separate, well‑audited routine that calls this
      validator first.
    """
    if not isinstance(usr_cmd, str):
        # Non‑string input cannot be a valid command.
        return None

    cleaned_cmd = usr_cmd.strip()
    if not cleaned_cmd:
        # Empty or whitespace‑only input is considered invalid.
        return None

    if cleaned_cmd in ALLOWED_COMMANDS:
        # The command is explicitly allowed.
        return cleaned_cmd

    # Command not found in the whitelist.
    return None


# --------------------------------------------------------------------------- #
# Example usage (for manual testing only).  Remove or comment out before
# integrating into a production system.
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_commands = [
        "list_files",
        "   show_date  ",
        "DROP TABLE users",          # malicious attempt
        "",
        "unknown_command",
    ]

    for cmd in test_commands:
        result = check_and_execute_command(cmd)
        if result is not None:
            print(f"ALLOWED: {result}")
        else:
            print(f"DENIED: {cmd!r}")