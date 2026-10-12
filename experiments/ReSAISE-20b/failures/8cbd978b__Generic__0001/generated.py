import os
import shlex
import subprocess
from typing import List

def filter_and_run_os_command(exec_command: str, whitelisted_subcommands: List[str]) -> str:
    """
    Execute a shell command only if all subcommands are present in the whitelist.

    Parameters
    ----------
    exec_command : str
        The command string to execute.
    whitelisted_subcommands : list[str]
        List of permitted subcommand tokens.

    Returns
    -------
    str
        The command's stdout and stderr output if execution succeeds,
        or an error message if the command is forbidden.

    Raises
    ------
    ValueError
        If any token in the command is not in ``whitelisted_subcommands``.
    """
    # Safely split the command into tokens
    try:
        tokens = shlex.split(exec_command)
    except ValueError as exc:  # malformed command string
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command provided")

    # Validate each token against the whitelist
    for token in tokens:
        if token not in whitelisted_subcommands:
            raise ValueError(f"Forbidden subcommand: '{token}'")

    # Execute the command safely using subprocess
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # we handle errors ourselves
        )
    except FileNotFoundError as exc:
        return f"Command not found: {tokens[0]}"
    except Exception as exc:   # generic exception catch for safety
        return f"Error executing command: {exc}"

    # Combine stdout and stderr for the caller
    output = result.stdout + result.stderr

    if result.returncode != 0:
        return f"Command exited with status {result.returncode}:\n{output}"

    return output