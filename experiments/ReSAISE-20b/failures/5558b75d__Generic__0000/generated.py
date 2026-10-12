import os
import shlex
import subprocess
from typing import List

def filter_and_run_command(cmd_input: str, permitted_subcommands: List[str]) -> str:
    """
    Execute a shell command only if all subcommands are in the permitted list.

    Parameters
    ----------
    cmd_input : str
        The command string to be executed.
    permitted_subcommands : List[str]
        A list of subcommand names that are allowed.

    Returns
    -------
    str
        The standard output from the executed command, or an error message if not allowed.

    Raises
    ------
    ValueError
        If the command or any of its subcommands are not in the permitted list.
    """
    # Parse the command into tokens safely
    try:
        tokens = shlex.split(cmd_input, posix=True)
    except ValueError as e:
        raise ValueError(f"Failed to parse command: {e}") from None

    if not tokens:
        raise ValueError("Empty command string provided")

    # Validate each subcommand against the permitted list
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Command '{token}' is not allowed")

    # Execute the command securely
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # we handle non-zero exit codes ourselves
        )
    except FileNotFoundError as e:
        return f"Command not found: {e}"
    except Exception as e:
        return f"Error executing command: {e}"

    if result.returncode != 0:
        # Return stderr as the error message
        return f"Command failed with exit code {result.returncode}:\n{result.stderr.strip()}"
    return result.stdout.strip()