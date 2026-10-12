import re
from typing import Optional

# Define a set of trusted commands.  Only these will be allowed.
ALLOWED_COMMANDS = {
    "list",
    "show",
    "status",
    "help",
    # Add other safe commands here
}

# Regular expression that matches a simple command consisting only of lowercase letters.
# This prevents accidental injection via shell metacharacters or spaces.
_COMMAND_RE = re.compile(r"^[a-z]+$")


def validate_and_run_cmd(usr_command: str) -> Optional[str]:
    """
    Validate a user supplied command against a whitelist of safe commands.

    Parameters
    ----------
    usr_command : str
        The command string supplied by the user.

    Returns
    -------
    Optional[str]
        The command if it is present in ``ALLOWED_COMMANDS`` and matches the
        simple pattern; otherwise, ``None``.

    Notes
    -----
    The function does *not* execute the command.  It merely performs a
    validation step to guard against injection attacks (CWE‑74).  The returned
    string can safely be passed to downstream code that expects a single
    keyword command.
    """
    # Strip leading/trailing whitespace to avoid accidental mismatches.
    cmd = usr_command.strip()

    # Ensure the command contains only allowed characters (lowercase letters).
    if not _COMMAND_RE.match(cmd):
        return None

    # Perform the whitelist check.
    if cmd in ALLOWED_COMMANDS:
        return cmd
    return None