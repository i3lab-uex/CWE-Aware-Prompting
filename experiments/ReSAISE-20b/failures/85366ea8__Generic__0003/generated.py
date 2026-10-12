# Safe command checker

from typing import Optional, List


# Predefined list of commands that the user is allowed to execute.
ALLOWED_COMMANDS: List[str] = [
    "list",
    "show",
    "delete",
    "create",
    "update",
]

def check_and_execute_command(usr_cmd: str) -> Optional[str]:
    """
    Validate the user's command against a whitelist of allowed commands.

    Parameters
    ----------
    usr_cmd : str
        The command string entered by the user.

    Returns
    -------
    Optional[str]
        The original command if it is in ALLOWED_COMMANDS, otherwise None.

    Notes
    -----
    - The check is case-sensitive; if you need a case-insensitive comparison,
      adjust the logic accordingly.
    - No command is executed here; this function only performs validation.
    """
    if usr_cmd in ALLOWED_COMMANDS:
        return usr_cmd
    return None