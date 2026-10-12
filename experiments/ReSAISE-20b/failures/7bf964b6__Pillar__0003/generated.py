import os
import shlex
import subprocess
from typing import List

def validate_and_execute_command(shell_cmd: str, safe_subcommands: List[str]) -> str:
    """
    Validate that every subcommand in *shell_cmd* is present in
    *safe_subcommands*.  If validation passes, execute the command using
    subprocess.run without invoking a shell and return its stdout as a string.

    Parameters
    ----------
    shell_cmd : str
        The command line to validate and run.
    safe_subcommands : list[str]
        A list of subcommand names that are considered safe.

    Returns
    -------
    str
        The stdout produced by the command if it executed successfully.
        If validation fails, a ValueError is raised.

    Raises
    ------
    ValueError
        If *shell_cmd* is empty or if any token in the command does not match an
        element of *safe_subcommands*.
    RuntimeError
        If the command fails to execute (non-zero exit status).
    """
    if not shell_cmd.strip():
        raise ValueError("Empty command is not allowed.")

    # Split the command into tokens safely (no shell expansion)
    try:
        cmd_tokens = shlex.split(shell_cmd, posix=True)
    except ValueError as e:
        raise ValueError(f"Failed to parse command: {e}") from e

    if not cmd_tokens:
        raise ValueError("Command contains no tokens after parsing.")

    # Validate each token against the allowed subcommands
    for token in cmd_tokens:
        if token not in safe_subcommands:
            raise ValueError(f"Command '{token}' is not permitted.")

    # Execute the command safely (no shell)
    try:
        result = subprocess.run(
            cmd_tokens,
            capture_output=True,
            text=True,
            check=False  # We handle non-zero exit manually
        )
    except FileNotFoundError as e:
        raise RuntimeError(f"Command not found: {e}") from e

    if result.returncode != 0:
        raise RuntimeError(
            f"Command exited with non-zero status {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout.strip()