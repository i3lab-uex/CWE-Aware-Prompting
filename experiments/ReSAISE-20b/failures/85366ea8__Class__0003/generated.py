# check_and_execute_command.py

"""
Utility to validate user‑issued commands against a whitelist.

The function `check_and_execute_command` receives a string representing
a command that the user wants to run.  It returns the same string if it
exactly matches one of the pre‑defined allowed commands, otherwise it
returns `None`.  This prevents accidental or malicious injection of
arbitrary shell commands.

The list `ALLOWED_COMMANDS` should contain only the exact strings that
are permitted.  No interpolation or string formatting is performed,
so no special characters from the user input can alter the meaning
of a command (CWE‑74 mitigated).
"""

from __future__ import annotations

# Define the whitelist of commands that are safe to execute.
ALLOWED_COMMANDS = [
    "list_users",
    "show_status",
    "restart_service",
    "shutdown_system",
    "backup_data",
]

def check_and_execute_command(usr_cmd: str) -> str | None:
    """
    Validate a user command against the allowed commands list.

    Parameters
    ----------
    usr_cmd : str
        The command string supplied by the user.

    Returns
    -------
    str | None
        The original command if it is allowed; otherwise `None`.

    Notes
    -----
    * Comparison is performed using exact string equality to avoid
      partial matches or injection.
    * The function does not perform any escaping or shell quoting,
      as it never passes the command to a shell.  The caller must
      handle execution in a secure manner.
    """
    # Strip surrounding whitespace to avoid accidental mismatches
    cmd = usr_cmd.strip()

    # Exact match check against the whitelist
    if cmd in ALLOWED_COMMANDS:
        return cmd

    # If not found, deny execution
    return None


# Example usage (remove or guard with `if __name__ == "__main__":` in real code)
if __name__ == "__main__":
    test_commands = ["list_users", "rm -rf /", "  show_status ", "invalid_cmd"]
    for cmd in test_commands:
        result = check_and_execute_command(cmd)
        print(f"Input: {cmd!r} -> Result: {result}")