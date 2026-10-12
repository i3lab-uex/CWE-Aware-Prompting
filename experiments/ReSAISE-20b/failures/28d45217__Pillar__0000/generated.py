#!/usr/bin/env python3
"""
Utility to validate and execute shell commands against a whitelist of subcommands.
"""

import os
import shlex
import subprocess
from typing import List


def validate_and_execute_command(
    input_command: str,
    permitted_subcommands: List[str]
) -> str:
    """
    Execute a shell command only if every subcommand token is in the permitted list.

    Parameters
    ----------
    input_command : str
        The command string supplied by the user.
    permitted_subcommands : List[str]
        A list of allowed subcommand tokens.

    Returns
    -------
    str
        The stdout output of the command, or an error message if validation fails.

    Raises
    ------
    ValueError
        If the command is empty or any token is not in ``permitted_subcommands``.
    """
    # Strip leading/trailing whitespace
    command = input_command.strip()
    if not command:
        raise ValueError("No command provided.")

    # Use shlex to safely split the command into tokens
    try:
        tokens = shlex.split(command)
    except ValueError as exc:
        # Raised if the command string is malformed (e.g. unmatched quotes)
        raise ValueError(f"Malformed command: {exc}") from exc

    # Validate each token against the permitted list
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(
                f"Forbidden subcommand detected: '{token}'. "
                "Only the following are allowed: "
                f"{', '.join(permitted_subcommands)}"
            )

    # Execute the command safely without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False  # we handle non-zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        # The executable itself is not found
        raise ValueError(f"Command not found: {exc}") from exc

    # Build a user‑friendly output
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        # Include stderr for debugging but mask the actual command to avoid leaking
        return (
            f"Command failed with exit code {result.returncode}.\n"
            f"Error output:\n{result.stderr.strip()}"
        )


# Example usage (commented out to prevent accidental execution)
if __name__ == "__main__":
    allowed = ["echo", "ls", "-l", "/tmp"]
    try:
        output = validate_and_execute_command("echo Hello World", allowed)
        print(output)
    except ValueError as e:
        print(f"Validation error: {e}")