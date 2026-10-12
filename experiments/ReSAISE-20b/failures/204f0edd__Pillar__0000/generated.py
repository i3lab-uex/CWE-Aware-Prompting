import logging
from typing import Optional

# Configure basic logger for debugging purposes.
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

# Define a set of allowed commands.  Add or remove commands as needed.
ALLOWED_COMMANDS = {
    "start",
    "stop",
    "restart",
    "status",
    "reload",
}

def check_and_run_command(command: str) -> Optional[str]:
    """
    Validate a user-supplied command against a whitelist of allowed commands.

    Parameters
    ----------
    command : str
        The raw user input that may represent a command.

    Returns
    -------
    Optional[str]
        The original command string if it is in ALLOWED_COMMANDS; otherwise, None.

    Notes
    -----
    - This function performs a strict membership test against ALLOWED_COMMANDS.
      No string manipulation or pattern matching is performed, preventing
      accidental execution of unintended commands.
    - The command string is returned unchanged if it passes validation; any
      further processing or execution should be handled by the caller.
    - Logging is used to trace invalid attempts, which can aid in monitoring
      potential misuse or attacks.
    """
    # Strip leading/trailing whitespace to avoid accidental mismatches
    cleaned_command = command.strip()

    if cleaned_command in ALLOWED_COMMANDS:
        logging.debug(f"Command '{cleaned_command}' is authorized.")
        return cleaned_command

    # Log the attempt for audit purposes
    logging.warning(f"Unauthorized command attempt: '{cleaned_command}'")
    return None