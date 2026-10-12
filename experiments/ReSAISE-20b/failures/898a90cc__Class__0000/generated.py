#!/usr/bin/env python3
"""
Utility to validate user supplied commands against a whitelist of safe commands.
"""

from typing import Optional

# Define the set of allowed command strings.
ALLOWED_COMMANDS = {
    "list",
    "show",
    "help",
    "status",
    # Add more safe commands as needed
}

def verify_and_run_command(cmd_input: str) -> Optional[str]:
    """
    Validate a user supplied command against the whitelist of safe commands.

    Parameters
    ----------
    cmd_input : str
        The command string supplied by the user.

    Returns
    -------
    Optional[str]
        The original command string if it is in the whitelist, otherwise None.
    
    Notes
    -----
    - The function performs a strict membership test against the ALLOWED_COMMANDS set.
    - No execution or system call is performed; this function only verifies the command.
    - By returning None for disallowed commands, downstream code can decide how to handle
      unauthorized input without risking command injection.
    """
    # Normalise the input by stripping leading/trailing whitespace
    cleaned = cmd_input.strip()

    if cleaned in ALLOWED_COMMANDS:
        return cleaned
    else:
        # Command not authorized; safe to reject
        return None

# Example usage (for demonstration only, remove or guard under __main__ in production)
if __name__ == "__main__":
    test_cmds = ["list", "delete", " show ", "invalid; rm -rf /"]
    for cmd in test_cmds:
        result = verify_and_run_command(cmd)
        if result is not None:
            print(f"Authorized command: {result}")
        else:
            print(f"Unauthorized or malformed command rejected: {cmd!r}")