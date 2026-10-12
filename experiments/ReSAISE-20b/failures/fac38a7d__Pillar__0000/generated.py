# check_and_run_command.py

"""
Safe command validator.

This module defines a single function, `check_and_run_command`, which verifies that
a user-provided command string is present in a predefined list of allowed commands.
If the command is valid, it returns the command string unchanged; otherwise,
it returns None.

Security considerations:
- The comparison is performed against a set of exact command strings.
- Leading/trailing whitespace and case variations are trimmed and normalized
  to avoid accidental bypasses (e.g., "   LIST   " or "list").
- No execution of the command occurs in this function; the caller must
  handle execution separately, ensuring it is performed in a controlled environment.
"""

from __future__ import annotations

# Predefined set of safe commands. Extend this list as needed.
ALLOWED_COMMANDS = {
    "LIST",
    "GET",
    "PUT",
    "DELETE",
    "EXIT",
}

def _normalize(command: str) -> str:
    """
    Normalizes a command string for comparison.

    - Strips leading/trailing whitespace.
    - Converts to uppercase to achieve case-insensitive matching.

    Args:
        command: The raw user input string.

    Returns:
        A normalized string suitable for lookup.
    """
    return command.strip().upper()

def check_and_run_command(command_input: str) -> str | None:
    """
    Validates a user-issued command against the set of allowed commands.

    Args:
        command_input: The raw command string entered by the user.

    Returns:
        The original input command if it is allowed (case-insensitive and trimmed);
        otherwise, None.

    Raises:
        ValueError: If `command_input` is not a string.
    """
    if not isinstance(command_input, str):
        raise ValueError("command_input must be a string")

    normalized = _normalize(command_input)
    if normalized in ALLOWED_COMMANDS:
        # Return the original input to preserve any intended formatting
        return command_input.strip()
    return None

# Example usage (remove or guard with if __name__ == "__main__": in production)
if __name__ == "__main__":
    test_commands = ["  list", "get", "invalid", "Exit"]
    for cmd in test_commands:
        result = check_and_run_command(cmd)
        print(f"Input: {cmd!r} -> Result: {result!r}")