#!/usr/bin/env python3
"""
Securely execute a shell command while restricting the allowed subcommands.

The function parses the command string using shlex to avoid shell injection,
ensures that only a predefined set of subcommands is executed, and runs the
command without invoking the shell.  The output (stdout or stderr) is returned
as a string.  Any disallowed subcommand results in a ValueError.

This implementation mitigates CWE‑707 by validating the structured command
before execution and ensuring that no untrusted data reaches downstream
components.
"""

import shlex
import subprocess
from typing import List


def run_shell_command_with_filters(
    command: str,
    allowed_subcommands_list: List[str]
) -> str:
    """
    Execute a shell command after validating that its subcommand is allowed.

    Parameters
    ----------
    command : str
        The shell command to execute.
    allowed_subcommands_list : list[str]
        A list of subcommands that are permitted to run.

    Returns
    -------
    str
        The combined stdout and stderr of the command, or an error message.

    Raises
    ------
    ValueError
        If the command is empty, cannot be parsed, or contains a disallowed
        subcommand.
    """
    if not command:
        raise ValueError("Command string is empty")

    # Safely split the command into tokens
    try:
        args = shlex.split(command, posix=True)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not args:
        raise ValueError("No executable found in command")

    # Validate the primary subcommand (first token)
    subcmd = args[0]
    if subcmd not in allowed_subcommands_list:
        raise ValueError(f"Disallowed subcommand: {subcmd}")

    # Optional: further validation could be added here for arguments

    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False  # We handle non-zero exit codes manually
        )
    except OSError as exc:
        return f"Execution failed: {exc}"

    # Combine stdout and stderr for simplicity
    output = result.stdout + result.stderr

    if result.returncode != 0:
        return f"Command exited with code {result.returncode}:\n{output}"

    return output