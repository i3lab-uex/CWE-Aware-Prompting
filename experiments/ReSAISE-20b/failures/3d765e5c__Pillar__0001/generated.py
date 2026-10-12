import os
import shlex
import subprocess
from typing import List

def filtered_system_command(cmd: str, approved_cmd_list: List[str]) -> str:
    """
    Execute a shell command after validating each subcommand against an approved list.

    Parameters
    ----------
    cmd : str
        The user-supplied shell command to execute.
    approved_cmd_list : list[str]
        A collection of permitted subcommands that can be run.

    Returns
    -------
    str
        The command's standard output if execution succeeds, otherwise the error message.

    Raises
    ------
    ValueError
        If any token in ``cmd`` is not present in ``approved_cmd_list`` or if the command
        string is empty/whitespace only.
    """
    # Strip leading/trailing whitespace and ensure the command isn't empty
    stripped_cmd = cmd.strip()
    if not stripped_cmd:
        raise ValueError("Command is empty or contains only whitespace.")

    # Tokenize the command safely without invoking a shell
    try:
        tokens = shlex.split(stripped_cmd)
    except ValueError as exc:  # e.g., unmatched quotes
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    # Validate each token against the approved list
    for token in tokens:
        if token not in approved_cmd_list:
            raise ValueError(f"Disallowed subcommand detected: '{token}'")

    # Execute the command using subprocess without shell=True to avoid injection
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,          # decode bytes to str using locale encoding
            check=False         # we handle non-zero exit codes manually
        )
    except FileNotFoundError as exc:
        # The first token (the executable) was not found
        raise ValueError(f"Executable not found: {exc}") from exc
    except PermissionError as exc:
        raise ValueError(f"Permission denied while executing: {exc}") from exc

    # If the command exited with a non-zero status, return stderr as error message
    if result.returncode != 0:
        # Prefer stderr over stdout for errors, but include both for context
        error_msg = result.stderr.strip() or result.stdout.strip()
        return f"Command failed with exit code {result.returncode}:\n{error_msg}"

    # Successful execution: return stdout
    return result.stdout.strip()