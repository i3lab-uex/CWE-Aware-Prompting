# List of commands that are considered safe for execution.
ALLOWED_COMMANDS = {
    "start",
    "stop",
    "restart",
    "status",
    "help",
}

def validate_and_run_cmd(usr_command: str):
    """
    Validate a user-provided command against the set of allowed commands.

    Parameters
    ----------
    usr_command : str
        The command string entered by the user.

    Returns
    -------
    str | None
        The original command string if it is in ALLOWED_COMMANDS;
        otherwise, None.
    """
    # Perform an exact match; no string interpolation or concatenation is used
    # to avoid CWE-74 (command injection).  The command is returned only if it
    # is exactly one of the pre-approved strings.
    return usr_command if usr_command in ALLOWED_COMMANDS else None