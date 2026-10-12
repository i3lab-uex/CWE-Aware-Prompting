from __future__ import annotations

# Define the set of commands that are considered safe.
ALLOWED_COMMANDS = {
    "list",
    "show",
    "create",
    "delete",
    "update",
    # Add any additional safe commands here.
}

def run_command_if_safe(user_command: str) -> str | None:
    """
    Validate a user-supplied command against a whitelist of allowed commands.

    Parameters
    ----------
    user_command : str
        The command string supplied by the user.

    Returns
    -------
    str | None
        The original command if it is in ALLOWED_COMMANDS; otherwise, None.
    """
    # Normalise the command: strip whitespace and lower-case for comparison.
    normalized = user_command.strip().lower()

    # Check against the whitelist.
    if normalized in ALLOWED_COMMANDS:
        return user_command  # Return the original string for further processing.
    return None