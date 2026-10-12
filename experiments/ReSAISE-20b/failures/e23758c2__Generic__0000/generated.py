#!/usr/bin/env python3
"""
Utility to safely execute a shell command only if all its subcommands are permitted.
"""

import shlex
import subprocess
from typing import List


def validate_and_execute_command(
    input_command: str, permitted_subcommands: List[str]
) -> str:
    """
    Execute a shell command only if every token in the command is present
    in `permitted_subcommands`.

    Parameters
    ----------
    input_command : str
        The command string supplied by the user.
    permitted_subcommands : list[str]
        A list of tokens that are allowed to appear in the command.

    Returns
    -------
    str
        Combined stdout and stderr from the executed command.

    Raises
    ------
    ValueError
        If any token in the parsed command is not found in `permitted_subcommands`.
    """
    # Split the command safely into tokens.
    try:
        tokens = shlex.split(input_command)
    except ValueError as exc:  # malformed quoting
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command provided")

    # Validate each token.
    for tok in tokens:
        if tok not in permitted_subcommands:
            raise ValueError(f"Unauthorized subcommand: {tok!r}")

    # Execute the command without invoking a shell.
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # we handle errors via return code
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {tokens[0]!r}") from exc

    # Combine stdout and stderr for the caller.
    output = result.stdout
    if result.stderr:
        output += "\n" + result.stderr

    return output


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    allowed = ["echo", "ls", "-l", "/tmp"]
    try:
        out = validate_and_execute_command("echo Hello, world!", allowed)
        print(out)
    except ValueError as e:
        print(f"Command rejected: {e}")