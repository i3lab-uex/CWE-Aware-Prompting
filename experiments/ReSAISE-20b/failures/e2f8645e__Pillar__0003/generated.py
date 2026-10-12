import os
import shlex
import subprocess
from typing import List

def execute_command_with_restrictions(cmd: str, approved_subcommands: List[str]) -> str:
    """
    Execute a shell command only if every subcommand token is in the approved list.

    Parameters
    ----------
    cmd : str
        The command line to be executed.
    approved_subcommands : list[str]
        A list of subcommand tokens that are allowed to be used.

    Returns
    -------
    str
        The stdout of the command if executed successfully,
        or an error message indicating that the command was not allowed.

    Raises
    ------
    ValueError
        If any token in the command is not present in ``approved_subcommands``.
    """
    # Split the command into tokens safely
    try:
        tokens = shlex.split(cmd, posix=True)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command provided")

    # Validate every token against the approved list
    for token in tokens:
        if token not in approved_subcommands:
            raise ValueError(f"Command or subcommand '{token}' is not allowed")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # Do not raise on non-zero exit
        )
    except FileNotFoundError as exc:
        return f"Command not found: {exc}"
    except Exception as exc:   # pragma: no cover
        return f"Execution failed: {exc}"

    if result.returncode != 0:
        # Return stderr as error message
        return f"Command failed with exit code {result.returncode}:\n{result.stderr.strip()}"
    return result.stdout.strip()