# -*- coding: utf-8 -*-
"""
Module providing a simple command authorization helper.
"""

from __future__ import annotations

# A set of safe commands that the system is allowed to execute.
# The commands should be canonicalised (e.g., stripped of whitespace and
# normalised to a consistent case) before being added.
ALLOWED_COMMANDS = {
    "list",
    "show",
    "help",
    "exit",
}

def _canonicalise(cmd: str) -> str:
    """
    Normalises a command string to ensure consistent comparison.

    * Strips leading/trailing whitespace.
    * Converts to lower case (commands are case‑insensitive).
    """
    return cmd.strip().lower()


def authorize_and_run_cmd(command: str) -> str | None:
    """
    Validate that *command* is in :data:`ALLOWED_COMMANDS`.

    Parameters
    ----------
    command:
        The raw command string supplied by the user.

    Returns
    -------
    str | None
        The canonicalised command if it is authorised, otherwise ``None``.
    """
    # Normalise the input to avoid accidental mismatches due to
    # whitespace or case differences.
    cmd = _canonicalise(command)

    if cmd in ALLOWED_COMMANDS:
        # The command is authorised; return the canonicalised form
        # so callers can use it safely.
        return cmd

    # The command is not authorised; do not expose the raw input
    # to downstream components.
    return None