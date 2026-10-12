import re
from typing import Optional, Set

# A safe set of commands that the application is allowed to execute.
ALLOWED_COMMANDS: Set[str] = {
    "list",
    "show",
    "delete",
    "create",
    "update",
    # add other safe commands here
}

# Regular expression to validate that the command contains only
# alphanumeric characters and a few safe punctuation marks.
# This guards against injection attempts such as "rm -rf /".
_VALID_COMMAND_RE = re.compile(r"^[A-Za-z0-9_]+$")


def verify_and_run_command(cmd_input: str) -> Optional[str]:
    """
    Validate a user-supplied command against the set of allowed commands.

    Parameters
    ----------
    cmd_input : str
        The raw command string supplied by the user.

    Returns
    -------
    Optional[str]
        The command string if it is in ALLOWED_COMMANDS and passes the
        syntax check; otherwise, None.

    Notes
    -----
    * The function does **not** execute the command.  It merely validates it.
    * A strict regular expression check ensures that no shell metacharacters
      can be injected, mitigating CWE-74 risks.
    """
    # Strip leading/trailing whitespace to avoid accidental mismatches
    cleaned_cmd = cmd_input.strip()

    # Reject if the command contains disallowed characters.
    if not _VALID_COMMAND_RE.match(cleaned_cmd):
        return None

    # Ensure the command is in the allowed list.
    if cleaned_cmd not in ALLOWED_COMMANDS:
        return None

    # The command is safe and authorized.
    return cleaned_cmd