import shlex

# Define the list of commands that are considered safe for execution.
ALLOWED_COMMANDS = [
    "list",
    "show",
    "status",
    "restart",
    "stop",
]

def validate_and_execute_command(cmd: str) -> str | None:
    """
    Validate a user-provided command against a whitelist of allowed commands.

    Parameters
    ----------
    cmd : str
        The raw command string supplied by the user.

    Returns
    -------
    str | None
        The command if it is in ALLOWED_COMMANDS; otherwise, None.

    Notes
    -----
    * The function performs a strict equality check after normalizing whitespace.
    * It does not allow any arguments or sub‑commands; only the base command name is permitted.
    * This design prevents injection attacks (CWE‑74) by ensuring that only
      pre‑approved, known command strings are ever passed to the execution layer.
    """
    # Strip leading/trailing whitespace and collapse internal spaces.
    cleaned_cmd = " ".join(shlex.split(cmd))

    # Only allow a single word that matches the whitelist.
    if cleaned_cmd in ALLOWED_COMMANDS:
        return cleaned_cmd

    # Command not allowed; return None to indicate failure.
    return None