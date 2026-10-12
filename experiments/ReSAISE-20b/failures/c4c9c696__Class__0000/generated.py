# -*- coding: utf-8 -*-
"""
Utility to validate user supplied commands against a whitelist.

The function `check_and_run_command` accepts a string from the user and
returns it only if it matches one of the commands in `ALLOWED_COMMANDS`.
Otherwise, it returns None.  This protects against command injection
(CWE‑74) by ensuring that only explicitly permitted commands are ever
executed or forwarded.

Author: OpenAI ChatGPT
"""

# Define the set of commands that are considered safe.
ALLOWED_COMMANDS = {
    "list_files",
    "show_status",
    "restart_service",
    "shutdown_system",
    # Add more allowed commands here as needed.
}

def check_and_run_command(user_input: str) -> str | None:
    """
    Validate the user input against a whitelist of allowed commands.

    Parameters
    ----------
    user_input : str
        The raw command string supplied by the user.

    Returns
    -------
    str | None
        The validated command if it is in ALLOWED_COMMANDS; otherwise, None.
    """
    # Strip surrounding whitespace to avoid accidental mismatches
    cleaned_input = user_input.strip()

    # Use a set lookup for O(1) performance and deterministic behaviour
    if cleaned_input in ALLOWED_COMMANDS:
        return cleaned_input

    # If the command is not allowed, do not expose any details to downstream
    # components; simply return None.
    return None

# Example usage (commented out to keep module import-safe)
# if __name__ == "__main__":
#     cmd = input("Enter command: ")
#     result = check_and_run_command(cmd)
#     if result:
#         print(f"Executing command: {result}")
#     else:
#         print("Command not allowed.")