#!/usr/bin/env python3
"""
A small utility to safely run shell commands with user‑supplied arguments.

The function uses ``subprocess.run`` without ``shell=True`` so that the
arguments are passed directly to the executable, avoiding shell injection
issues (CWE‑77).  All inputs are validated and any failure results in a
``ValueError`` containing the relevant error message.
"""

import subprocess
from typing import List


def run_command(cmd: str, cmd_arguments: List[str]) -> str:
    """
    Execute a command with the supplied arguments and return its output.

    Parameters
    ----------
    cmd : str
        The main executable to run (e.g., "ls", "python").
    cmd_arguments : list
        A list of string arguments to pass to the executable.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If ``cmd`` or any argument is not a string, if the command fails to
        execute, or if the command returns a non‑zero exit status.
    """
    # Basic type validation
    if not isinstance(cmd, str):
        raise ValueError("Command must be a string")
    if not isinstance(cmd_arguments, list) or any(
        not isinstance(a, str) for a in cmd_arguments
    ):
        raise ValueError("Arguments must be a list of strings")

    # Build the command list; do not use shell=True to avoid injection
    full_cmd = [cmd] + cmd_arguments

    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            check=True,          # Raises CalledProcessError on non‑zero exit
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {cmd}") from e
    except subprocess.CalledProcessError as e:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command '{cmd}' failed with exit code {e.returncode}:\n{e.stderr}"
        ) from e
    except Exception as e:
        # Catch any other unexpected errors
        raise ValueError(f"Unexpected error running command '{cmd}': {e}") from e

    return result.stdout