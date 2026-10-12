import re
from typing import Optional

# Define the set of safe commands.  In practice this should be populated with
# real, vetted commands for the specific application.
ALLOWED_COMMANDS = {
    "list",
    "status",
    "restart",
    "shutdown",
}

# Regular expression that matches a command consisting only of
# letters, digits, hyphens and underscores.
_COMMAND_RE = re.compile(r"^[A-Za-z0-9_-]+$")

def run_command_if_safe(user_command: str) -> Optional[str]:
    """
    Validate that the user supplied command is safe to run.

    Parameters
    ----------
    user_command : str
        The raw command string supplied by the user.

    Returns
    -------
    Optional[str]
        The original command if it is in ALLOWED_COMMANDS and passes
        the basic sanitisation checks.  Otherwise, None.

    Notes
    -----
    * The command is stripped of leading/trailing whitespace.
    * Only commands that match the allowed set are accepted.
    * A simple regex is used to reject any characters that could be
      interpreted specially by downstream command‑executing code,
      mitigating injection risks (CWE‑74).
    """
    # Trim whitespace
    cmd = user_command.strip()

    # Reject if the command contains disallowed characters
    if not _COMMAND_RE.match(cmd):
        return None

    # Check against the allowed set
    if cmd in ALLOWED_COMMANDS:
        return cmd

    # Not authorised
    return None