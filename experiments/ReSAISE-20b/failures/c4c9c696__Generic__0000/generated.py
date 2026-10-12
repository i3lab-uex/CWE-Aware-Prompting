#!/usr/bin/env python3
"""
Secure command validator.

This module defines `check_and_run_command`, which verifies that a user-supplied
command is in the trusted whitelist `ALLOWED_COMMANDS`.  If the command is
allowed, it is returned unchanged; otherwise, `None` is returned.

The function performs only a simple membership test and does not execute
the command.  Execution should be handled by the caller if needed.
"""

from __future__ import annotations

import logging
from typing import Optional, Iterable

# Configure a basic logger for debugging / auditing purposes.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Define the set of commands that are considered safe.
ALLOWED_COMMANDS: frozenset[str] = frozenset(
    [
        "list",
        "status",
        "restart",
        "shutdown",
        "backup",
    ]
)


def check_and_run_command(user_input: str) -> Optional[str]:
    """
    Validate the user-supplied command against a whitelist.

    Parameters
    ----------
    user_input : str
        The raw command string supplied by the user.

    Returns
    -------
    Optional[str]
        The original command if it is in `ALLOWED_COMMANDS`; otherwise,
        ``None``.
    """
    # Normalise input: strip whitespace and collapse internal spaces.
    command = " ".join(user_input.strip().split())

    if command in ALLOWED_COMMANDS:
        logger.debug(f"Command allowed: {command!r}")
        return command

    logger.warning(f"Attempted to use disallowed command: {command!r}")
    return None


# Example usage (for manual testing only):
if __name__ == "__main__":
    test_inputs = [
        "list",
        "  status  ",
        "update",
        "shutdown now",  # not allowed because of the extra argument
    ]

    for inp in test_inputs:
        result = check_and_run_command(inp)
        print(f"Input: {inp!r} -> Result: {result!r}")