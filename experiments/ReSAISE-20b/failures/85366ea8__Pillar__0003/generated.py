from typing import Optional, Iterable

# Predefined list of commands that the user is allowed to run.
ALLOWED_COMMANDS = {
    "list",
    "status",
    "restart",
    "shutdown",
    "help",
}

def check_and_execute_command(usr_cmd: str) -> Optional[str]:
    """
    Validate a user-issued command against the set of allowed commands.

    Parameters
    ----------
    usr_cmd : str
        The raw command string entered by the user.

    Returns
    -------
    Optional[str]
        The original command string if it is in ALLOWED_COMMANDS,
        otherwise None.

    Notes
    -----
    * The comparison is case-sensitive; if you wish to allow
      different capitalisations, convert both sides to a common
      case (e.g. lower()) before comparison.
    * This function **does not** execute the command; it merely
      validates that the command is permitted.  Execution should be
      performed by a separate, carefully audited routine.
    * The function uses a set for O(1) membership checks and
      protects against injection attacks by never evaluating the
      command string as code.
    """
    # Strip surrounding whitespace to avoid accidental mismatches.
    cleaned_cmd = usr_cmd.strip()

    if cleaned_cmd in ALLOWED_COMMANDS:
        return cleaned_cmd
    else:
        return None