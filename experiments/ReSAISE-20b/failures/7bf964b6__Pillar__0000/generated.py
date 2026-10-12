#!/usr/bin/env python3
"""
validate_and_execute_command

Executes a shell command only if every token in the command string is present
in a supplied list of safe subcommands.  The implementation uses shlex to
split the command safely and subprocess.run with shell=False to avoid shell
injection.  Any disallowed token causes a ValueError.

The function returns the command's stdout on success or an error message
indicating why it was rejected.
"""

import shlex
import subprocess
from typing import List


def validate_and_execute_command(shell_cmd: str, safe_subcommands: List[str]) -> str:
    """
    Execute a shell command only if all its tokens are in the list of safe subcommands.

    Args:
        shell_cmd: The command string to execute.
        safe_subcommands: A list of allowed subcommand tokens.

    Returns:
        The stdout of the executed command, or an error message if the
        command was not allowed.

    Raises:
        ValueError: If any token in the command is not in safe_subcommands.
    """
    # Split the command into tokens safely
    try:
        tokens = shlex.split(shell_cmd, posix=True)
    except ValueError as exc:
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command is not allowed")

    # Validate each token against the whitelist
    for idx, token in enumerate(tokens):
        if token not in safe_subcommands:
            raise ValueError(
                f"Disallowed subcommand '{token}' at position {idx} "
                f"not in the safe list"
            )

    # Execute the command safely (no shell expansion)
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # We handle non-zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        return f"Command not found: {exc}"
    except Exception as exc:  # pragma: no cover
        return f"Execution error: {exc}"

    if result.returncode != 0:
        # Return stderr on failure
        return f"Command failed (exit {result.returncode}):\n{result.stderr.strip()}"

    return result.stdout.strip()