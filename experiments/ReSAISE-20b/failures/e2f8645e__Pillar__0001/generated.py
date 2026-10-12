import os
import shlex
import subprocess
from typing import List

def execute_command_with_restrictions(cmd: str, approved_subcommands: List[str]) -> str:
    """
    Execute a shell command only if all sub‑components are approved.

    Parameters
    ----------
    cmd : str
        The command string to be executed.
    approved_subcommands : List[str]
        A list of allowed sub‑command names (e.g., ['ls', 'echo']).

    Returns
    -------
    str
        The stdout of the executed command.

    Raises
    ------
    ValueError
        If any part of the command is not in `approved_subcommands` or if the command fails.
    """
    # Split the command safely into arguments
    try:
        args = shlex.split(cmd, posix=True)
    except ValueError as e:          # malformed quoting
        raise ValueError(f"Command syntax error: {e}") from e

    if not args:
        raise ValueError("Empty command")

    # Verify that every subcommand (here we consider the first token as the main command)
    # and any explicit subcommands in the list are approved.
    for token in args:
        # Treat only the first word as a command; others are arguments.
        if token in approved_subcommands:
            continue
        # If the token is not an approved subcommand but matches a known pattern like 'git commit',
        # we can add more sophisticated checks here. For now, reject any token not explicitly approved.
        if token in {'--help', '-h'}:  # allow common flags
            continue
        raise ValueError(f"Subcommand '{token}' is not approved")

    # Execute the command safely (no shell expansion)
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False,          # We handle errors manually
            cwd=os.getcwd()
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {e}") from e
    except Exception as e:
        raise ValueError(f"Execution failed: {e}") from e

    if result.returncode != 0:
        raise ValueError(
            f"Command failed with return code {result.returncode}:\n{result.stderr}"
        )

    return result.stdout