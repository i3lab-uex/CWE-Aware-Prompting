#!/usr/bin/env python3
"""
Utility to safely execute a shell command with strict subcommand filtering.
"""

import os
import shlex
import subprocess
from typing import List


def run_shell_command_with_filters(
    command: str,
    allowed_subcommands_list: List[str],
) -> str:
    """
    Execute a shell command after ensuring all subcommands are in the allowed list.

    Parameters
    ----------
    command : str
        The shell command to run (e.g. "ls -l /tmp").
    allowed_subcommands_list : list[str]
        A list of subcommand tokens that are permitted. The first token
        (the executable) must also be present in this list.

    Returns
    -------
    str
        Combined stdout and stderr of the command, or an error message if
        execution fails.

    Raises
    ------
    ValueError
        If the command contains any token not present in ``allowed_subcommands_list``.
    """
    if not isinstance(command, str):
        raise ValueError("command must be a string")

    # Safely split the command into tokens
    try:
        tokens = shlex.split(command)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command provided")

    # Ensure every token is in the allowed list
    disallowed = [t for t in tokens if t not in allowed_subcommands_list]
    if disallowed:
        raise ValueError(
            f"Disallowed subcommand(s) detected: {', '.join(disallowed)}"
        )

    # Execute the command without invoking a shell for security
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # We handle non-zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        return f"Executable not found: {exc}"
    except Exception as exc:
        return f"Error executing command: {exc}"

    output = result.stdout + result.stderr
    if result.returncode != 0:
        output += f"\nCommand exited with return code {result.returncode}"

    return output.strip()


# Example usage
if __name__ == "__main__":
    allowed = ["echo", "-n", "Hello, World!"]
    try:
        print(run_shell_command_with_filters("echo -n Hello, World!", allowed))
    except ValueError as err:
        print(f"Security error: {err}")