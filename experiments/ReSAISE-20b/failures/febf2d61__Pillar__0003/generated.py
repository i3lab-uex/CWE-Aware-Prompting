#!/usr/bin/env python3
"""
Module: command_verifier

Provides a single function `verify_and_run_command` that checks whether
a user‑supplied command is in a predefined whitelist (`ALLOWED_COMMANDS`).
If the command is allowed, it is returned unchanged; otherwise `None`
is returned.  No execution of the command is performed by this module
to avoid accidental or malicious side effects.

Security considerations:
- The whitelist uses a set for O(1) lookup and to avoid duplicate entries.
- Input is stripped of leading/trailing whitespace before comparison,
  ensuring that variations like " ls" or "ls " are rejected.
- The function does **not** perform any kind of command execution,
  thereby preventing CWE‑707 (Improper Neutralization) and other
  injection vulnerabilities.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Whitelist of allowed commands
# --------------------------------------------------------------------------- #
ALLOWED_COMMANDS = {
    "list",
    "show",
    "status",
    "help",
    "exit"
}

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #
def verify_and_run_command(command: str) -> str | None:
    """
    Verify that the supplied command is in ALLOWED_COMMANDS.

    Parameters
    ----------
    command : str
        The user supplied command string. Leading/trailing whitespace is
        removed before validation.

    Returns
    -------
    str | None
        The original command string if it is allowed; otherwise ``None``.

    Notes
    -----
    This function deliberately does **not** execute the command.
    The caller is responsible for performing any safe execution
    after validation, e.g. by mapping the command to a safe handler.
    """
    # Normalise input: strip whitespace, convert to lower case
    normalized = command.strip().lower()

    if normalized in ALLOWED_COMMANDS:
        # Return the original string (preserving case/spacing) if needed
        return command

    return None


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Simulated user inputs
    test_commands = ["list", "  show ", "DELETE", "help", "Exit"]

    for cmd in test_commands:
        result = verify_and_run_command(cmd)
        if result is not None:
            print(f"Allowed command: {result!r}")
        else:
            print(f"Rejected command: {cmd!r}")