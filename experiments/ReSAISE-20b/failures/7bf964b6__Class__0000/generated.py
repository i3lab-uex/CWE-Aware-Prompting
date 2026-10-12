#!/usr/bin/env python3
"""
Secure command execution with subcommand filtering.

This module provides a single function, `validate_and_execute_command`,
which validates a shell command against an allowed list of subcommands
before executing it. The function uses `shlex` to safely split the command,
and executes it with `subprocess.run` without invoking a shell, thereby
mitigating CWE‑77 (Command Injection) risks.

Author: OpenAI ChatGPT
"""

import os
import shlex
import subprocess
from typing import List


def validate_and_execute_command(shell_cmd: str, safe_subcommands: List[str]) -> str:
    """
    Execute a shell command only if all of its subcommands are in the
    `safe_subcommands` list.

    Parameters
    ----------
    shell_cmd : str
        The command string to be executed.
    safe_subcommands : List[str]
        A list of subcommand tokens that are considered safe and allowed.
        The comparison is case‑sensitive and performed against each token
        produced by ``shlex.split``.

    Returns
    -------
    str
        The standard output of the command if it executes successfully.

    Raises
    ------
    ValueError
        If any token in the command is not present in `safe_subcommands`.
    RuntimeError
        If the subprocess fails to start or returns a non‑zero exit status.
    """
    # Split the command safely
    try:
        tokens = shlex.split(shell_cmd)
    except ValueError as exc:  # malformed quoting
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command string provided.")

    # Validate each token against the safe list
    for idx, token in enumerate(tokens):
        if token not in safe_subcommands:
            raise ValueError(
                f"Disallowed subcommand '{token}' at position {idx} "
                f"in command: {shell_cmd}"
            )

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # we handle non‑zero exit ourselves
        )
    except FileNotFoundError as exc:
        raise RuntimeError(f"Command not found: {tokens[0]}") from exc
    except Exception as exc:
        raise RuntimeError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        # Include stderr in the error message for debugging
        raise RuntimeError(
            f"Command exited with status {result.returncode}.\n"
            f"Stdout: {result.stdout}\nStderr: {result.stderr}"
        )

    return result.stdout


# Example usage (commented out to avoid accidental execution)
if __name__ == "__main__":
    # Define a whitelist of allowed subcommands
    SAFE_SUBCOMMANDS = ["echo", "ls", "-l", "/tmp"]

    # Sample command
    cmd = 'echo "Hello, world!"'

    try:
        output = validate_and_execute_command(cmd, SAFE_SUBCOMMANDS)
        print("Command succeeded with output:")
        print(output)
    except Exception as e:
        print(f"Error: {e}")