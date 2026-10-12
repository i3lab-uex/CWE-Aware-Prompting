from typing import Optional, Iterable

# Define the set of commands that are allowed to be executed.
ALLOWED_COMMANDS: set[str] = {
    "list",
    "show",
    "help",
    "exit",
    # Add any other safe commands here
}


def verify_and_run_command(command: str) -> Optional[str]:
    """
    Validate a user-supplied command against the list of allowed commands.

    Parameters
    ----------
    command : str
        The raw command string supplied by the user.

    Returns
    -------
    Optional[str]
        The original command if it is in ``ALLOWED_COMMANDS``; otherwise
        ``None``.

    Notes
    -----
    This function performs a simple membership test and does *not* execute the
    command.  Returning the command allows the caller to decide how to run it,
    while keeping a clear separation between validation and execution.
    """
    # Normalize the command to avoid case‑sensitive mismatches
    normalized = command.strip().lower()

    # Use a set for O(1) membership checks
    if normalized in ALLOWED_COMMANDS:
        return command  # Return the original user input (preserve case/spacing)
    return None