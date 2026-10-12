#!/usr/bin/env python3
"""
Utility to execute a shell command only if all of its subcommands are approved.
"""

import os
import shlex
import subprocess
from typing import List


def execute_command_with_restrictions(cmd: str, approved_subcommands: List[str]) -> str:
    """
    Execute a command only if all tokens (subcommands) are in the approved list.

    Parameters
    ----------
    cmd : str
        The command string to be executed.
    approved_subcommands : list[str]
        A list of allowed subcommand tokens.  All tokens produced by
        shlex.split(cmd) must be present in this list.

    Returns
    -------
    str
        The decoded standard output of the command if it executes successfully.

    Raises
    ------
    ValueError
        If any token in the command is not present in ``approved_subcommands``.
    subprocess.CalledProcessError
        If the command execution fails (non‑zero exit status).
    """
    # Split the command safely into tokens
    try:
        tokens = shlex.split(cmd)
    except ValueError as exc:  # pragma: no cover
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command is not allowed")

    # Ensure every token is approved
    for token in tokens:
        if token not in approved_subcommands:
            raise ValueError(
                f"Command '{token}' is not in the list of approved subcommands."
            )

    # Execute the command without invoking a shell
    result = subprocess.run(
        tokens,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,  # Raise CalledProcessError on non-zero exit
    )

    return result.stdout.decode("utf-8", errors="replace")


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     approved = ["echo", "-n", "Hello, World!"]
#     try:
#         output = execute_command_with_restrictions('echo -n "Hello, World!"', approved)
#         print("Command output:", output)
#     except Exception as e:
#         print(f"Error: {e}")