# validate_and_run_cmd.py

"""
Utility to validate user supplied commands against a whitelist of trusted commands.
"""

from typing import Optional, Set

# Define the set of allowed commands.  In a real system this would be
# populated from configuration or environment variables and could contain
# more complex command strings.  Here we keep it simple for illustration.
ALLOWED_COMMANDS: Set[str] = {
    "list_files",
    "show_status",
    "restart_service",
    "backup_data",
}

def validate_and_run_cmd(usr_command: str) -> Optional[str]:
    """
    Validate a user supplied command against the trusted whitelist.

    Parameters
    ----------
    usr_command : str
        The raw command string supplied by the user.

    Returns
    -------
    Optional[str]
        The original command if it is in `ALLOWED_COMMANDS`; otherwise, None.

    Notes
    -----
    - The comparison is performed using exact string equality.
      No further sanitisation is required because we never construct a
      new command from user input; we simply check membership.
    - If the command is not allowed, None is returned to indicate
      that no action should be taken.
    """
    # Strip leading/trailing whitespace and normalize newline characters
    cleaned = usr_command.strip()

    # Check for membership in the allowed set.
    if cleaned in ALLOWED_COMMANDS:
        return cleaned
    else:
        return None

# Example usage (would normally be in a separate test module)
if __name__ == "__main__":
    for cmd in ["list_files", "delete_all", "restart_service   ", ""]:
        result = validate_and_run_cmd(cmd)
        if result is not None:
            print(f"Executing allowed command: {result}")
        else:
            print(f"Ignored disallowed or empty command: '{cmd}'")