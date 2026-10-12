#!/usr/bin/env python3
"""
Validate a user-provided command against an allowlist before execution.

The function `validate_and_execute_command` ensures that only commands
present in the global `ALLOWED_COMMANDS` list are permitted. It performs
basic sanity checks to mitigate CWE-707 (Improper Neutralization of Structured
Data) by ensuring the command is a string, stripping surrounding whitespace,
and rejecting empty inputs. If the command is allowed it is returned;
otherwise `None` is returned.

The caller should use this return value to decide whether to execute the
command, e.g. via `subprocess.run()` or similar.
"""

from typing import Optional

# Define the set of allowed commands.  In a real system this list should
# be curated carefully and may include only safe, non‑privileged commands.
ALLOWED_COMMANDS = [
    "echo",
    "ls",
    "pwd",
    "date",
]

def validate_and_execute_command(cmd: str) -> Optional[str]:
    """
    Validate the supplied command against ALLOWED_COMMANDS.

    Parameters
    ----------
    cmd : str
        The user-provided command string.

    Returns
    -------
    Optional[str]
        The original command if it is allowed; otherwise None.
    """
    # Ensure cmd is a string
    if not isinstance(cmd, str):
        return None

    # Trim surrounding whitespace to avoid accidental mismatches
    cmd_clean = cmd.strip()

    # Reject empty commands
    if not cmd_clean:
        return None

    # Check against the allowlist (case-sensitive)
    if cmd_clean in ALLOWED_COMMANDS:
        return cmd_clean

    # Command not allowed
    return None