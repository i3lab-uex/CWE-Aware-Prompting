from typing import Optional

# Predefined set of commands that are considered safe to run.
ALLOWED_COMMANDS = [
    "list",
    "show",
    "delete",
    "create",
    "update",
    # Add more allowed commands here as needed.
]

def check_and_run_command(command_input: str) -> Optional[str]:
    """
    Validate a user-provided command against a whitelist of allowed commands.

    Parameters
    ----------
    command_input : str
        The raw string entered by the user.

    Returns
    -------
    Optional[str]
        The command string if it is in ALLOWED_COMMANDS; otherwise, None.

    Notes
    -----
    * The comparison is case-sensitive and requires an exact match.
    * Leading/trailing whitespace is ignored to avoid accidental mismatches.
    """
    # Strip surrounding whitespace to make the check user‑friendly
    command = command_input.strip()

    if command in ALLOWED_COMMANDS:
        return command
    return None