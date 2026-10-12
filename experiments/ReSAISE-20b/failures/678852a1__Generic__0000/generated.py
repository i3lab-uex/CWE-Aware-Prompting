import shlex

# Define the list of commands that are allowed to be executed.
ALLOWED_COMMANDS = [
    "ls",
    "pwd",
    "whoami",
    "date",
    # Add more safe commands as needed
]

def validate_and_execute_command(cmd: str) -> str | None:
    """
    Validate a user-provided command against a whitelist of allowed commands.

    Parameters
    ----------
    cmd : str
        The user-provided command to validate.

    Returns
    -------
    str | None
        The original command if it is in the whitelist; otherwise ``None``.
    """
    # Strip leading/trailing whitespace and normalize spacing
    normalized = shlex.split(cmd.strip())
    if not normalized:
        return None

    # The command is considered valid only if the first token matches an allowed command
    # and no additional arguments are present (or you can extend this logic).
    if normalized[0] in ALLOWED_COMMANDS and len(normalized) == 1:
        return cmd.strip()
    return None