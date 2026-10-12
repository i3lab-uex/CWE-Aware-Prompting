import os
import shlex
import subprocess
from typing import List

def filter_and_run_os_command(exec_command: str, whitelisted_subcommands: List[str]) -> str:
    """
    Execute a shell command only if all subcommands are in the whitelist.

    Parameters
    ----------
    exec_command : str
        The command string to execute.
    whitelisted_subcommands : list[str]
        A list of allowed subcommand tokens.

    Returns
    -------
    str
        The command's stdout and stderr combined, or an error message if the
        command is forbidden.

    Raises
    ------
    ValueError
        If any subcommand in the command is not present in `whitelisted_subcommands`.
    """
    if not exec_command.strip():
        raise ValueError("Empty command")

    # Safely split the command into tokens
    try:
        tokens = shlex.split(exec_command)
    except ValueError as exc:  # e.g., unmatched quotes
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    # Validate each token against the whitelist
    for token in tokens:
        if token not in whitelisted_subcommands:
            raise ValueError(f"Forbidden subcommand: {token}")

    # Execute the command using a subprocess
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # we handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {tokens[0]}") from exc
    except Exception as exc:
        raise ValueError(f"Execution failed: {exc}") from exc

    # Combine stdout and stderr for a single string result
    output = result.stdout + result.stderr

    return output if output else "Command executed with no output."