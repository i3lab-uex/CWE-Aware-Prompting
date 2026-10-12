#!/usr/bin/env python3
"""
Securely validate and execute a shell command.

The function ensures that every token in the command is present in a
user‑supplied whitelist of permitted subcommands before executing it.
It uses the `subprocess` module with `shell=False` to avoid shell
injection vulnerabilities.

CWE‑707: Improper Neutralization – the function explicitly checks each
token and refuses to execute commands that contain unapproved tokens.
"""

import shlex
import subprocess
from typing import List


def validate_and_execute_command(
    input_command: str,
    permitted_subcommands: List[str],
) -> str:
    """
    Execute a shell command only if all subcommands are permitted.

    Parameters
    ----------
    input_command : str
        The command string provided by the user.
    permitted_subcommands : list[str]
        A whitelist of allowed subcommand tokens.

    Returns
    -------
    str
        The combined stdout and stderr output of the executed command.

    Raises
    ------
    ValueError
        If `input_command` is empty or any token in the command is not
        found in ``permitted_subcommands``.
    """
    if not input_command:
        raise ValueError("Empty command is not allowed")

    # Split the command into tokens safely (no shell interpretation)
    try:
        tokens = shlex.split(input_command, posix=True)
    except ValueError as exc:  # malformed command
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("Command contains no executable tokens")

    # Verify every token against the whitelist
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Token '{token}' is not permitted")

    # Execute the command securely
    try:
        completed = subprocess.run(
            tokens,
            capture_output=True,
            text=True,          # decode output to str
            check=False,        # we handle non‑zero return codes ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Executable not found: {tokens[0]}") from exc
    except Exception as exc:
        raise ValueError(f"Execution failed: {exc}") from exc

    # Combine stdout and stderr for the caller
    output = completed.stdout + completed.stderr
    return output


# Example usage (remove or guard with __name__ == "__main__" in real code)
if __name__ == "__main__":
    whitelist = ["echo", "ls", "-l", "/"]
    try:
        result = validate_and_execute_command("echo Hello, world!", whitelist)
        print(result)
    except ValueError as err:
        print(f"Command rejected: {err}")