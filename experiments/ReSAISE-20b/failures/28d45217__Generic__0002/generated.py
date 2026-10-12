#!/usr/bin/env python3
"""
Utility module for safely executing shell commands with a whitelist of allowed subcommands.
"""

import shlex
import subprocess
from typing import List

def validate_and_execute_command(
    input_command: str,
    permitted_subcommands: List[str]
) -> str:
    """
    Execute a shell command only if all subcommands are in the permitted list.

    Parameters
    ----------
    input_command : str
        The raw command string supplied by the user.
    permitted_subcommands : List[str]
        A list of subcommand names that are allowed to be executed.

    Returns
    -------
    str
        The standard output of the command if successful, or an error message.

    Raises
    ------
    ValueError
        If the command contains a subcommand not in `permitted_subcommands`.
    """
    # Tokenise the input safely
    try:
        tokens = shlex.split(input_command)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command provided")

    # The first token is the primary command (e.g., 'git', 'ls')
    primary = tokens[0]
    if primary not in permitted_subcommands:
        raise ValueError(f"Command '{primary}' is not permitted")

    # Validate all subcommands (tokens after the primary)
    for sub in tokens[1:]:
        if sub not in permitted_subcommands:
            raise ValueError(f"Subcommand '{sub}' is not permitted")

    # Execute the command safely
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False  # We handle errors ourselves
        )
    except FileNotFoundError as exc:
        return f"Command not found: {exc}"
    except Exception as exc:
        return f"Execution failed: {exc}"

    # Build the response
    if result.returncode != 0:
        return (
            f"Command failed with exit code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )
    return result.stdout.strip()


# Example usage (commented out to avoid accidental execution)
# if __name__ == "__main__":
#     allowed = ["echo", "ls", "-l", "/tmp"]
#     print(validate_and_execute_command("echo Hello World", allowed))