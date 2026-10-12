# Safe command validation module

ALLOWED_COMMANDS = [
    "list",          # e.g., list files
    "status",        # check status
    "restart",       # restart service
    "update",        # update system
    "help"           # show help information
]

def check_and_run_command(command_input: str) -> str | None:
    """
    Validate a user-issued command against the predefined ALLOWED_COMMANDS list.

    Parameters
    ----------
    command_input : str
        The raw string entered by the user.

    Returns
    -------
    str | None
        The command string if it is allowed, otherwise None.

    Notes
    -----
    - Only exact matches are accepted; no partial or case-insensitive matching.
    - No command execution is performed here to avoid security risks.
    """
    # Normalize input: strip whitespace and keep original case
    cmd = command_input.strip()

    if cmd in ALLOWED_COMMANDS:
        return cmd

    # Command not allowed
    return None