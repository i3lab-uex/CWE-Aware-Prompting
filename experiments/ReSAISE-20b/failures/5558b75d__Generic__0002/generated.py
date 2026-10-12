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
        The command string to execute.
    permitted_subcommands : list of str
        Subcommands that are considered safe.

    Returns
    -------
    str
        The command's standard output on success, or an error message.

    Raises
    ------
    ValueError
        If the command contains a subcommand that is not permitted.
    """
    # Split the command safely
    try:
        parts = shlex.split(cmd_input)
    except ValueError as exc:  # malformed command
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not parts:
        raise ValueError("Empty command")

    # Validate each subcommand
    for token in parts[1:]:  # skip the base command itself
        if token not in permitted_subcommands:
            raise ValueError(f"Command '{token}' is not allowed")

    # Execute the command
    try:
        result = subprocess.run(
            parts,
            capture_output=True,
            text=True,
            check=False,  # we handle non-zero exit ourselves
        )
    except FileNotFoundError as exc:
        return f"Command not found: {exc}"
    except OSError as exc:
        return f"Execution error: {exc}"

    # Return stdout or stderr based on exit code
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Command failed with exit code {result.returncode}:\n{result.stderr.strip()}"