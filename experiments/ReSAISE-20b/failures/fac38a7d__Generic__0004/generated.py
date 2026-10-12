# safe_command_executor.py

"""
A minimal, secure helper for validating user-provided commands against a whitelist.

The module defines `ALLOWED_COMMANDS` – a tuple of exact command strings that are permitted.
`check_and_run_command()` checks if the supplied input matches one of these commands and
returns it for further processing. If the command is not allowed, `None` is returned.

No external libraries are required; the implementation relies only on built‑in Python
features, making it safe from common injection attacks. The function performs a strict,
case‑sensitive comparison and trims surrounding whitespace to avoid accidental mismatches.
"""

from typing import Optional

# Predefined whitelist of safe commands
ALLOWED_COMMANDS = (
    "list",
    "show",
    "delete",
    "update",
    "create",
)

def check_and_run_command(command_input: str) -> Optional[str]:
    """
    Validate a user-supplied command against the allowed list.

    Parameters
    ----------
    command_input : str
        The raw string entered by the user. Leading/trailing whitespace is ignored.

    Returns
    -------
    Optional[str]
        The command string if it is in `ALLOWED_COMMANDS`; otherwise, None.
    """
    # Normalize input: strip whitespace but keep the original command for return
    normalized = command_input.strip()

    # Perform a strict, case-sensitive membership test
    if normalized in ALLOWED_COMMANDS:
        return normalized

    # Command not allowed; safely reject
    return None


# Example usage (uncomment to test):
#
# if __name__ == "__main__":
#     user_input = input("Enter command: ")
#     cmd = check_and_run_command(user_input)
#     if cmd:
#         print(f"Executing safe command: {cmd}")
#     else:
#         print("Invalid or disallowed command.")