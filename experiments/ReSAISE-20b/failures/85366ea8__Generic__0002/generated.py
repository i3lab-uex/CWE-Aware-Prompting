# Safe command checker

from typing import Optional, List

# Define the set of commands that are allowed to be executed.
# In a real application this list should be kept up‑to‑date and
# only contain commands that are known to be safe.
ALLOWED_COMMANDS: List[str] = [
    "list_files",
    "show_date",
    "display_uptime",
    # Add more safe commands here
]

# Convert the list to a set for O(1) membership checks.
_ALLOWED_COMMANDS_SET = set(ALLOWED_COMMANDS)


def check_and_execute_command(usr_cmd: str) -> Optional[str]:
    """
    Validate a user‑supplied command against the whitelist of allowed commands.

    Parameters
    ----------
    usr_cmd : str
        The command string supplied by the user.

    Returns
    -------
    Optional[str]
        The original command if it is in ALLOWED_COMMANDS, otherwise None.

    Notes
    -----
    - The function deliberately does **not** execute the command.
      It only performs a safety check. Execution should be handled
      elsewhere with additional safeguards (e.g., subprocess checks,
      environment isolation, etc.).
    - Membership is checked against a set for efficiency.
    """
    # Strip whitespace and normalize the command string
    cmd = usr_cmd.strip()

    if cmd in _ALLOWED_COMMANDS_SET:
        return cmd

    # Command not allowed
    return None