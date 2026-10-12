import os
import shlex
import subprocess
from typing import List


def run_shell_command_with_filters(
    command: str, allowed_subcommands_list: List[str]
) -> str:
    """
    Execute a shell command only if its first token (subcommand)
    is present in the allowed_subcommands_list.

    Parameters
    ----------
    command : str
        The shell command to execute.
    allowed_subcommands_list : list[str]
        A list of permitted subcommand names (e.g. ["git", "ls"]).

    Returns
    -------
    str
        The stdout output of the command if it succeeds, otherwise an error message.

    Raises
    ------
    ValueError
        If the command is empty, contains disallowed subcommands,
        or if the execution fails (non‑zero exit status).
    """
    # Strip whitespace and validate command is not empty
    if not command or not command.strip():
        raise ValueError("Command string must not be empty")

    # Safely split the command into arguments
    try:
        args = shlex.split(command)
    except ValueError as exc:  # e.g. unmatched quotes
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not args:
        raise ValueError("Command could not be parsed into arguments")

    # The first token is considered the subcommand to check
    subcommand = args[0]
    if subcommand not in allowed_subcommands_list:
        raise ValueError(f"Disallowed subcommand: '{subcommand}'")

    # Execute the command without invoking a shell for safety
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False,  # We'll handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Executable not found: {subcommand}") from exc
    except OSError as exc:
        raise ValueError(f"OS error while executing command: {exc}") from exc

    # If the process failed, raise a ValueError with stderr
    if result.returncode != 0:
        err_msg = (
            f"Command '{command}' failed with exit code {result.returncode}\n"
            f"stderr: {result.stderr.strip()}"
        )
        raise ValueError(err_msg)

    # Return the command's stdout
    return result.stdout.strip()