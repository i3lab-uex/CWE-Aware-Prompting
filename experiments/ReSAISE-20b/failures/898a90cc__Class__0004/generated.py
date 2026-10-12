import re

# Define a set of commands that are safe to execute.
ALLOWED_COMMANDS = {
    "list",
    "show",
    "status",
    "restart",
    "shutdown",
}

# Regular expression that matches a single command token with no special characters
_COMMAND_RE = re.compile(r"^[a-zA-Z0-9_-]+$")

def verify_and_run_command(cmd_input: str) -> str | None:
    """
    Validate a user-supplied command against a whitelist of safe commands.

    Parameters
    ----------
    cmd_input : str
        The raw command string entered by the user.

    Returns
    -------
    str | None
        The sanitized command if it is in the whitelist; otherwise, ``None``.

    Notes
    -----
    * The function strips leading/trailing whitespace.
    * It rejects any command that contains characters outside the allowed
      alphanumeric set or is not present in :data:`ALLOWED_COMMANDS`.
    * This protects against injection attacks such as CWE‑74 by ensuring that
      the command string cannot be manipulated to alter downstream parsing or
      execution semantics.
    """
    # Normalize whitespace and remove any surrounding spaces
    cmd = cmd_input.strip()

    # Quick reject if the command contains disallowed characters
    if not _COMMAND_RE.match(cmd):
        return None

    # Check against the whitelist
    if cmd not in ALLOWED_COMMANDS:
        return None

    # At this point the command is safe to use downstream
    return cmd