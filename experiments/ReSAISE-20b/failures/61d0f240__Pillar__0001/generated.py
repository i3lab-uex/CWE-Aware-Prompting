#!/usr/bin/env python3
"""
Utility to execute shell commands with strict subcommand whitelisting.

The function checks that each token in the user‑supplied command is
present in an approved list before invoking it.  It uses ``shlex.split``
to safely parse the command string and runs the process without
``shell=True`` to avoid shell injection.

CWE‑707: The function explicitly validates the structure of the command
before execution, ensuring that only approved subcommands are run.
"""

import os
import shlex
import subprocess
from typing import List


def execute_permitted_command(input_command: str, approved_commands: List[str]) -> str:
    """
    Execute a user‑supplied command only if all its tokens are in the
    approved_commands list.

    Parameters
    ----------
    input_command : str
        The raw command string supplied by the user.
    approved_commands : list[str]
        A collection of permitted subcommands (e.g., ['ls', 'echo']).

    Returns
    -------
    str
        The stdout of the executed command, or an error message if the
        execution fails.

    Raises
    ------
    ValueError
        If any token in the command is not present in approved_commands.
    """
    # Parse the command into a list of tokens safely
    try:
        cmd_parts = shlex.split(input_command)
    except ValueError as e:
        raise ValueError(f"Command parsing failed: {e}") from None

    if not cmd_parts:
        raise ValueError("No command provided")

    # Validate every token against the approved list
    for part in cmd_parts:
        if part not in approved_commands:
            raise ValueError(f"Unauthorized subcommand: {part!r}")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            cmd_parts,
            capture_output=True,
            text=True,
            check=False,  # We handle errors ourselves
        )
    except FileNotFoundError:
        return f"Command not found: {cmd_parts[0]!r}"
    except Exception as exc:
        return f"Execution error: {exc!s}"

    # Return stdout or stderr if the command failed
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        # Include stderr to aid debugging
        error_msg = result.stderr.strip() or "Unknown error"
        return f"Command failed with exit code {result.returncode}: {error_msg}"


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    approved = ["echo", "ls", "cat"]
    try:
        output = execute_permitted_command("echo Hello, world!", approved)
        print(output)
    except ValueError as ve:
        print(f"Permission error: {ve}")