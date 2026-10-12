# check_and_run_command.py

"""
This module provides a secure way to validate user supplied commands against
a predefined whitelist of allowed commands.

CWE-74: Improper Neutralization of Special Elements in Output Used by a Downstream Component
The implementation below mitigates injection risks by performing an exact match
against a set of allowed command strings. No user input is interpolated into any
command templates or executed directly.
"""

from typing import Optional

# A whitelist of commands that are considered safe to execute.
ALLOWED_COMMANDS = {
    "start",
    "stop",
    "restart",
    "status",
    "reload",
}

def check_and_run_command(user_input: str) -> Optional[str]:
    """
    Validate the user supplied command against a whitelist.

    Parameters
    ----------
    user_input : str
        The raw command string supplied by the user.

    Returns
    -------
    Optional[str]
        The validated command if it is in ALLOWED_COMMANDS; otherwise, None.
    """
    # Normalize input: strip surrounding whitespace and convert to lower case
    normalized = user_input.strip().lower()

    # Perform an exact match against the allowed set
    if normalized in ALLOWED_COMMANDS:
        return normalized

    # Command not permitted; return None to signal rejection
    return None


# Example usage (for demonstration purposes only)
if __name__ == "__main__":
    test_inputs = ["  Start  ", "SHUTDOWN", "status", "restart; rm -rf /"]
    for cmd in test_inputs:
        result = check_and_run_command(cmd)
        if result is not None:
            print(f"Executing allowed command: {result}")
        else:
            print(f"Ignored disallowed command: '{cmd}'")