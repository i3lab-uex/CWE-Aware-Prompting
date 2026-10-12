# -*- coding: utf-8 -*-

"""
A small helper that validates user supplied commands against a whitelist.
"""

from typing import Optional, Iterable

# Define the set of safe commands. Adjust as needed for your environment.
ALLOWED_COMMANDS: Iterable[str] = (
    "list",
    "status",
    "restart",
    "shutdown",
    "backup",
)

# Convert to a set for O(1) membership checks
_ALLOWED_COMMANDS_SET = set(ALLOWED_COMMANDS)


def authorize_and_run_cmd(command: str) -> Optional[str]:
    """
    Validate a user supplied command against the trusted whitelist.

    Parameters
    ----------
    command : str
        The raw command string supplied by the user.

    Returns
    -------
    Optional[str]
        The original command if it is allowed; otherwise ``None``.
    """
    # Strip surrounding whitespace and normalize to a single space between words
    cleaned = " ".join(command.strip().split())

    # Perform a case‑sensitive match against the whitelist
    if cleaned in _ALLOWED_COMMANDS_SET:
        return cleaned

    # Command is not permitted
    return None