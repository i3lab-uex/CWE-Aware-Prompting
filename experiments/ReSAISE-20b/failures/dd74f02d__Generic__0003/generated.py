# Safe command validation module

ALLOWED_COMMANDS = {
    "list",
    "status",
    "restart",
    "shutdown",
    "update",
}

def run_command_if_safe(user_command: str) -> str | None:
    """
    Validate a user-supplied command against a whitelist of allowed commands.

    Parameters
    ----------
    user_command : str
        The command entered by the user.

    Returns
    -------
    str | None
        The original command string if it is in the whitelist; otherwise ``None``.

    Notes
    -----
    - The check is case-sensitive to avoid accidental execution of unintended commands.
    - Leading and trailing whitespace are stripped before validation.
    """
    if not isinstance(user_command, str):
        return None

    cleaned = user_command.strip()
    return cleaned if cleaned in ALLOWED_COMMANDS else None