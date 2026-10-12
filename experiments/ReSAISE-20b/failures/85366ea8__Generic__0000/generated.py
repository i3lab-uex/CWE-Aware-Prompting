# Safe command checker – only allows predefined commands.
# No external imports are required.

from typing import Optional

# Define the set of allowed commands.  Adjust as needed.
ALLOWED_COMMANDS = {
    "list",
    "show",
    "help",
    "exit",
    # Add other safe commands here
}


def check_and_execute_command(usr_cmd: str) -> Optional[str]:
    """
    Validate a user-provided command against the list of allowed commands.

    Parameters
    ----------
    usr_cmd : str
        The command entered by the user.

    Returns
    -------
    Optional[str]
        The original command string if it is in ALLOWED_COMMANDS,
        otherwise None.

    Notes
    -----
    This function performs a simple membership test.  It does **not**
    execute the command; it merely checks that the command is safe
    according to the application's policy.
    """
    # Normalize input: strip whitespace and convert to lowercase
    cleaned_cmd = usr_cmd.strip().lower()

    if cleaned_cmd in ALLOWED_COMMANDS:
        return cleaned_cmd
    else:
        # Command not allowed – silently reject.
        return None