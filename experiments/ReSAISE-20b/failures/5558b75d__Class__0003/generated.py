import os
import shlex
import subprocess
from typing import List

def filter_and_run_command(cmd_input: str, permitted_subcommands: List[str]) -> str:
    """
    Execute a shell command only if its tokens are all present in the
    permitted_subcommands list.

    Parameters
    ----------
    cmd_input : str
        The command string supplied by the caller.
    permitted_subcommands : list of str
        A whitelist of allowed command tokens.  Every token in the parsed
        command must appear in this list; otherwise a ValueError is raised.

    Returns
    -------
    str
        The stdout of the executed command on success, or an error message
        if the command was not allowed.

    Raises
    ------
    ValueError
        If any token in the command is not found in ``permitted_subcommands``.
    """
    # Parse the command safely into tokens
    try:
        tokens = shlex.split(cmd_input)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command provided")

    # Verify every token against the whitelist
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Command '{token}' is not allowed")

    # Execute the command using a list of arguments (no shell expansion)
    try:
        result = subprocess.run(
            tokens,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,  # We handle errors ourselves
        )
    except OSError as exc:
        return f"Execution failed: {exc}"

    # Return the command output or an error message if it exited with a non‑zero status
    if result.returncode != 0:
        return f"Command failed with exit code {result.returncode}:\n{result.stdout}"
    return result.stdout