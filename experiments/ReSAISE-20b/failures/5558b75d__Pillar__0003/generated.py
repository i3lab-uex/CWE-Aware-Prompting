import shlex
import subprocess
from typing import List


def filter_and_run_command(cmd_input: str, permitted_subcommands: List[str]) -> str:
    """
    Execute a shell command only if all of its subcommands are in the permitted list.

    Parameters
    ----------
    cmd_input : str
        The raw command string supplied by the caller.
    permitted_subcommands : list[str]
        A list of safe subcommand names (e.g., ['ls', 'echo']).

    Returns
    -------
    str
        The standard output of the executed command.

    Raises
    ------
    ValueError
        If any part of the command is not in `permitted_subcommands` or if execution fails.
    """
    # Safely split the command into tokens (e.g., ["ls", "-l", "/tmp"])
    try:
        tokens = shlex.split(cmd_input, posix=True)
    except ValueError as exc:
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command provided")

    # Validate each token against the allowed subcommands list
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Command or subcommand '{token}' is not allowed")

    # Execute the command without invoking a shell (prevents shell injection)
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # We handle errors manually
        )
    except OSError as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        # Include stderr in the error message for better diagnostics
        raise ValueError(
            f"Command failed with exit code {result.returncode}:\n{result.stderr}"
        )

    return result.stdout