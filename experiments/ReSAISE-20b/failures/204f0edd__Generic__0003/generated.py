# safe_command_executor.py

from typing import Optional, Set


# Define the set of allowed commands.
ALLOWED_COMMANDS: Set[str] = {
    "list",
    "show",
    "help",
    "exit",
    "status",
    # Add more safe commands as needed
}


def check_and_run_command(command: str) -> Optional[str]:
    """
    Validate the user-supplied command against a predefined list of safe commands.

    Parameters
    ----------
    command : str
        The command string entered by the user.

    Returns
    -------
    Optional[str]
        The original command if it is in ALLOWED_COMMANDS; otherwise, None.

    Notes
    -----
    - The check is case-sensitive and does not allow leading/trailing whitespace.
      If you want to ignore surrounding whitespace, use ``command.strip()`` before
      calling this function.
    - This function only performs validation; it does not execute the command.
      Execution should be handled by another, trusted component that guarantees
      safe operation.
    """
    # Ensure the command is a string and strip any accidental whitespace.
    if not isinstance(command, str):
        return None

    cleaned_command = command.strip()

    # Return the command only if it is in the allowed set.
    return cleaned_command if cleaned_command in ALLOWED_COMMANDS else None