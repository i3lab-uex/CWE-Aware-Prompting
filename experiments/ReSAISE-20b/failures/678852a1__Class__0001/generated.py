#!/usr/bin/env python3
"""
Secure command validation module.

This module exposes a single function, `validate_and_execute_command`, which
ensures that any command supplied by a user is exactly one of the
pre‑defined, whitelisted commands.  The function returns the command if it is
allowed; otherwise it returns `None`.  No attempt is made to execute the command
here – that responsibility lies with a downstream component that will use the
validated string.

The implementation is intentionally strict:
* It compares the command string verbatim (after stripping surrounding whitespace).
* No additional arguments or shell metacharacters are accepted.
* The list of allowed commands is defined as a constant tuple for immutability.

The code follows the principle of least privilege and mitigates CWE‑74
(Injection) by refusing any command that is not an exact match to the allowed set.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Define a tuple of allowed commands.  Use an immutable type to prevent accidental
# modification at runtime.
ALLOWED_COMMANDS: tuple[str, ...] = (
    "list",
    "status",
    "restart",
    "shutdown",
)

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def validate_and_execute_command(cmd: str) -> str | None:
    """
    Validate a user‑supplied command against the whitelist of allowed commands.

    Parameters
    ----------
    cmd : str
        The raw command string supplied by the user.  Leading/trailing whitespace is ignored.

    Returns
    -------
    str | None
        The command string if it is exactly one of the allowed commands; otherwise `None`.

    Notes
    -----
    The function performs a *strict* equality check.  Any attempt to inject additional
    arguments, shell metacharacters, or whitespace will cause the command to be rejected.
    """
    # Normalise input by stripping leading/trailing whitespace
    cleaned_cmd = cmd.strip()

    # Reject empty strings early
    if not cleaned_cmd:
        return None

    # Perform a strict membership test against the immutable allowed set
    if cleaned_cmd in ALLOWED_COMMANDS:
        return cleaned_cmd

    # If the command is not allowed, do not expose any information about the
    # whitelist to avoid leaking internal implementation details.
    return None

# --------------------------------------------------------------------------- #
# Example usage (for demonstration only; remove or guard with `if __name__ == "__main__":` in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Example commands to test the validator
    test_commands = [
        "list",
        "status",
        "restart now",  # invalid: extra argument
        "shutdown; rm -rf /",  # invalid: injection attempt
        "   list   ",  # valid after stripping whitespace
    ]

    for cmd in test_commands:
        result = validate_and_execute_command(cmd)
        print(f"Input: {cmd!r} -> Validated: {result!r}")