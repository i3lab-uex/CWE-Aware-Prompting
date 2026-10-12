# Define the list of commands that are considered safe.
ALLOWED_COMMANDS = [
    "list",
    "show",
    "delete",
    "create",
    "update",
    "help"
]

def check_and_execute_command(usr_cmd: str) -> str | None:
    """
    Validate a user-issued command against the predefined set of safe commands.

    Parameters
    ----------
    usr_cmd : str
        The command string input by the user.

    Returns
    -------
    str | None
        The original command string if it is in ALLOWED_COMMANDS,
        otherwise ``None``.

    Notes
    -----
    - The check is case‑sensitive and requires an exact match.
    - Leading/trailing whitespace is ignored.
    - No command execution occurs in this function; it merely validates the input.
    """
    # Normalize whitespace: strip leading/trailing spaces
    cmd = usr_cmd.strip()

    # Use a set for O(1) membership tests and to avoid accidental duplicate checks.
    allowed_set = set(ALLOWED_COMMANDS)

    return cmd if cmd in allowed_set else None