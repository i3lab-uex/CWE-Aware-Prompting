import os
import shlex
import subprocess
from typing import List


def restricted_command_executor(user_command: str, whitelist_commands: List[str]) -> str:
    """
    Execute a user-supplied shell command only if all its components are in the whitelist.

    Parameters
    ----------
    user_command : str
        The command string entered by the user.
    whitelist_commands : List[str]
        A list of allowed subcommands or arguments.  Every token produced by
        shlex.split(user_command) must appear in this list, otherwise a
        ValueError is raised.

    Returns
    -------
    str
        The standard output of the command if it executes successfully.
        If an error occurs during execution, the error message is returned.

    Raises
    ------
    ValueError
        If any token in the command is not present in ``whitelist_commands``.
    """
    # Tokenise the user supplied command safely
    try:
        tokens = shlex.split(user_command)
    except ValueError as exc:
        # shlex raises ValueError for malformed input
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("No command supplied")

    # Ensure every token is in the whitelist
    for token in tokens:
        if token not in whitelist_commands:
            raise ValueError(f"Command '{token}' is not allowed")

    # Execute the command using subprocess.run
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # we handle non-zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        return f"Command not found: {exc}"
    except PermissionError as exc:
        return f"Permission denied: {exc}"

    # Return stdout on success, stderr otherwise
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        # Include the command that failed for debugging
        error_msg = (
            f"Command '{user_command}' exited with status {result.returncode}.\n"
            f"stderr:\n{result.stderr.strip()}"
        )
        return error_msg