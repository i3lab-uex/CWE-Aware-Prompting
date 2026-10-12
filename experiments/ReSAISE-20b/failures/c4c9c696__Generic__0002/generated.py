# SPDX-License-Identifier: MIT
"""
Utility to validate user supplied commands against a whitelist.
"""

from __future__ import annotations

import logging
from typing import Iterable, Optional

# Configure a module‑level logger (doesn't log by default)
logger = logging.getLogger(__name__)
# The default level is WARNING; users may adjust as needed.
logger.setLevel(logging.WARNING)

# Example whitelist – replace with your actual safe commands
ALLOWED_COMMANDS: set[str] = {
    "list",
    "show",
    "help",
    "exit",
    "status",
}

def check_and_run_command(user_input: str) -> Optional[str]:
    """
    Validate a user supplied command against the ALLOWED_COMMANDS set.

    Parameters
    ----------
    user_input : str
        The raw command string entered by the user.

    Returns
    -------
    Optional[str]
        The original `user_input` if it is present in the whitelist,
        otherwise ``None``.
    """
    # Normalise: strip whitespace and convert to lowercase
    command = user_input.strip().lower()

    if not command:
        logger.debug("Received empty command string.")
        return None

    # Check against the whitelist
    if command in ALLOWED_COMMANDS:
        logger.debug(f"Command '{command}' is allowed.")
        return command

    # Reject untrusted commands
    logger.warning(f"Untrusted command attempted: '{command}'.")
    return None


# Optional test block (removed if used as a library)
if __name__ == "__main__":
    # Simple interactive demo
    while True:
        inp = input("Enter command: ")
        result = check_and_run_command(inp)
        if result is None:
            print("Command not allowed.")
        else:
            print(f"Executing: {result}")