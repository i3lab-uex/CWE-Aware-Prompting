#!/usr/bin/env python3
"""
A utility to safely execute user supplied shell commands while enforcing a whitelist of allowed sub‑commands.

The function `restricted_command_executor` splits the input command using shlex, validates each token
against a provided whitelist and then runs it via `subprocess.run`.  If any token is not in the
whitelist, a ValueError is raised and no command is executed.

Note: This implementation still inherits the inherent risks of executing arbitrary shell
commands.  It should be used only when absolutely necessary and the whitelist must be carefully curated.
"""

import os
import shlex
import subprocess
from typing import List


def restricted_command_executor(user_command: str, whitelist_commands: List[str]) -> str:
    """
    Execute a user supplied shell command after ensuring all tokens are in the whitelist.

    Parameters
    ----------
    user_command : str
        The raw shell command provided by the user.
    whitelist_commands : List[str]
        A list of tokens that are permitted to appear in the command.

    Returns
    -------
    str
        The combined stdout and stderr of the executed command, or an error message if execution fails.

    Raises
    ------
    ValueError
        If any token in the parsed command is not present in ``whitelist_commands``.
    """
    if not isinstance(user_command, str):
        raise TypeError("user_command must be a string")
    if not isinstance(whitelist_commands, list):
        raise TypeError("whitelist_commands must be a list")

    # Tokenise the command safely
    try:
        tokens = shlex.split(user_command, posix=os.name != 'nt')
    except ValueError as e:
        return f"Invalid command syntax: {e}"

    if not tokens:
        return "No command provided."

    # Validate each token against the whitelist
    for token in tokens:
        if token not in whitelist_commands:
            raise ValueError(f"Command token '{token}' is not allowed.")

    # Execute the command
    try:
        completed = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # We handle non-zero exit codes ourselves
        )
    except FileNotFoundError:
        return f"Command '{tokens[0]}' not found."
    except Exception as exc:
        return f"Execution failed: {exc}"

    # Combine stdout and stderr
    output = completed.stdout.strip()
    error_output = completed.stderr.strip()

    if completed.returncode != 0:
        return f"Command exited with code {completed.returncode}.\nError: {error_output}"
    return output or "Command executed successfully with no output."