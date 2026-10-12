#!/usr/bin/env python3
"""
Secure command execution with subcommand whitelisting.

The function `filtered_system_command` verifies that every token in the
user‑supplied command is present in an approved list before executing it.
If any token is disallowed a ValueError is raised.  The command is run
using `subprocess.run` with `shell=False`, so the user cannot inject
arbitrary shell syntax.  The function returns the combined stdout and
stderr as a string, or an error message if execution fails.
"""

import shlex
import subprocess
from typing import List


def filtered_system_command(cmd: str, approved_cmd_list: List[str]) -> str:
    """
    Execute a shell command after validating that every token is in the
    approved list.

    Parameters
    ----------
    cmd : str
        The user‑supplied shell command to run.
    approved_cmd_list : List[str]
        A list of allowed subcommands (tokens).  The comparison is
        case‑sensitive and token‑based.

    Returns
    -------
    str
        The combined stdout and stderr of the executed command,
        or an error message if execution fails.

    Raises
    ------
    ValueError
        If any token in `cmd` is not present in `approved_cmd_list`.
    """
    # Split the command into individual tokens safely
    try:
        tokens = shlex.split(cmd, posix=True)
    except ValueError as e:  # shlex error (e.g., unmatched quotes)
        raise ValueError(f"Invalid command syntax: {e}") from e

    if not tokens:
        raise ValueError("No command specified")

    # Validate each token against the approved list
    for token in tokens:
        if token not in approved_cmd_list:
            raise ValueError(f"Disallowed command or argument: '{token}'")

    # Execute the command safely (no shell injection)
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # We handle non‑zero exit codes ourselves
        )
    except FileNotFoundError as e:
        return f"Command not found: {e}"
    except Exception as e:
        return f"Execution failed: {e}"

    # Return stdout and stderr combined
    output = result.stdout + result.stderr
    if not output:
        # If no output, still indicate exit status
        output = f"Command exited with return code {result.returncode}\n"
    else:
        output += f"\nCommand exited with return code {result.returncode}\n"

    return output