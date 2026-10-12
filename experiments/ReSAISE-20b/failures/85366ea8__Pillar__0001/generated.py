#!/usr/bin/env python3
"""
Utility to validate user-issued commands against a whitelist.

The module defines a single public function, :func:`check_and_execute_command`,
which checks whether the supplied command is present in a predefined set
of allowed commands.  If the command passes validation, it is returned
unchanged; otherwise ``None`` is returned.

The function deliberately avoids executing any commands directly.
Execution must be performed by the caller after a successful validation
step, ensuring that only whitelisted commands are run.

Security considerations:
- The command string is trimmed of leading/trailing whitespace.
- Case sensitivity is preserved; if case‑insensitive matching is desired,
  the caller can normalise both sides accordingly.
- The function uses a set for O(1) lookup performance and to avoid
  accidental duplicate entries.
- No external libraries are imported, preventing unintended side effects.

CWE-707: The function ensures that only well‑formed commands from the
whitelist are accepted, preventing improper neutralization of structured data.
"""

from __future__ import annotations

# Predefined list of allowed commands
ALLOWED_COMMANDS = [
    "list_files",
    "show_status",
    "restart_service",
    "shutdown_system",
]

# Convert to a set for efficient membership tests
_ALLOWED_COMMANDS_SET = frozenset(ALLOWED_COMMANDS)


def check_and_execute_command(usr_cmd: str) -> str | None:
    """
    Validate a user-provided command against the allowed command set.

    Parameters
    ----------
    usr_cmd : str
        The raw command string supplied by the user.

    Returns
    -------
    str | None
        The trimmed command if it is in :data:`ALLOWED_COMMANDS`; otherwise ``None``.

    Notes
    -----
    The function performs a simple membership test.  It does **not** execute
    the command; callers should handle execution after a successful check.
    """
    if not isinstance(usr_cmd, str):
        # Reject non-string input early
        return None

    cleaned = usr_cmd.strip()
    if cleaned in _ALLOWED_COMMANDS_SET:
        return cleaned
    return None


# Example usage (uncomment for testing)
if __name__ == "__main__":
    test_commands = [" list_files ", "invalid_command", "restart_service"]
    for cmd in test_commands:
        result = check_and_execute_command(cmd)
        print(f"Input: {cmd!r} -> Result: {result!r}")