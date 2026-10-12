import os
import shlex
import subprocess
from typing import List


def execute_permitted_command(input_command: str, approved_commands: List[str]) -> str:
    """
    Execute a shell command only if its primary subcommand is approved.

    Parameters
    ----------
    input_command : str
        The user‑supplied command string.
    approved_commands : List[str]
        A list of allowed primary subcommands (e.g. ['ls', 'cat']).

    Returns
    -------
    str
        Standard output of the command on success, or an error message.

    Raises
    ------
    ValueError
        If the primary subcommand is not in ``approved_commands``.
    """
    # Tokenise the command safely
    try:
        tokens = shlex.split(input_command, posix=True)
    except ValueError as exc:
        return f"Invalid command syntax: {exc}"

    if not tokens:
        return "No command provided."

    # Only the first token (the executable) must be approved.
    primary = tokens[0]
    if primary not in approved_commands:
        raise ValueError(
            f"Command '{primary}' is not permitted. "
            f"Allowed commands: {', '.join(approved_commands)}"
        )

    # Execute without invoking a shell to avoid injection
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # we handle errors ourselves
        )
    except FileNotFoundError:
        return f"Command '{primary}' not found on the system."
    except PermissionError:
        return f"Permission denied when executing '{primary}'."
    except Exception as exc:  # pragma: no cover
        return f"Unexpected error during execution: {exc}"

    if result.returncode != 0:
        # Include stderr for debugging
        return (
            f"Command exited with code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout.strip()