import os
import shlex
import subprocess
from typing import List

def execute_command_with_restrictions(cmd: str, approved_subcommands: List[str]) -> str:
    """
    Execute a shell command only if every token (command and subcommands) is in the approved list.

    Parameters
    ----------
    cmd : str
        The command string to execute.
    approved_subcommands : list of str
        A list of subcommand strings that are considered safe and permitted.

    Returns
    -------
    str
        The stdout of the executed command, or an error message if the command is not allowed.

    Raises
    ------
    ValueError
        If any token in the command is not present in `approved_subcommands`.
    """
    # Split the command into tokens safely.
    try:
        tokens = shlex.split(cmd, posix=True)
    except ValueError as exc:
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command")

    # Ensure every token is approved.
    for token in tokens:
        if token not in approved_subcommands:
            raise ValueError(f"Command or subcommand '{token}' is not allowed")

    # Execute the command without invoking a shell.
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # We handle non-zero exit ourselves.
        )
    except OSError as exc:
        return f"Execution failed: {exc}"

    # Return stdout on success, otherwise stderr.
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Command failed with exit code {result.returncode}:\n{result.stderr.strip()}"