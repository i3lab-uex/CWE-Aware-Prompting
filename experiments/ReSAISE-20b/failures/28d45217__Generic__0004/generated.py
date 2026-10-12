import os
import shlex
import subprocess
from typing import List

def validate_and_execute_command(input_command: str, permitted_subcommands: List[str]) -> str:
    """
    Execute a shell command only if all tokens (command and subcommands) are present in
    the list of permitted_subcommands.

    Parameters
    ----------
    input_command : str
        The command string to execute.
    permitted_subcommands : List[str]
        A list of allowed tokens. Each token from the parsed command must be in this
        list for execution to proceed.

    Returns
    -------
    str
        The stdout of the command if executed successfully, otherwise an error message.

    Raises
    ------
    ValueError
        If the command or any subcommand is not found in permitted_subcommands.
    """
    # Split input safely
    try:
        tokens = shlex.split(input_command)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command provided")

    # Validate each token
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Forbidden command or subcommand: '{token}'")

    # Execute the command securely
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False  # We will handle non-zero exit codes ourselves
        )
    except Exception as exc:
        return f"Execution failed: {exc}"

    # If command succeeded, return stdout; otherwise, include stderr
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Command failed with exit code {result.returncode}:\n{result.stderr.strip()}"