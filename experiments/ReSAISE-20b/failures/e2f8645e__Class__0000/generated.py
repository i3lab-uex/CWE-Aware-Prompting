import os
import shlex
import subprocess
from typing import List


def execute_command_with_restrictions(
    cmd: str, approved_subcommands: List[str]
) -> str:
    """
    Execute a shell command only if every token (subcommand) is in the approved list.

    Parameters
    ----------
    cmd : str
        The command string to be executed.
    approved_subcommands : list[str]
        A list of tokens that are considered safe and permitted.

    Returns
    -------
    str
        The stdout output of the command if it succeeds, otherwise an error message.

    Raises
    ------
    ValueError
        If the command is empty or any token is not in `approved_subcommands`.
    """
    if not cmd:
        raise ValueError("Command string is empty")

    # Split the command safely into tokens.
    try:
        tokens = shlex.split(cmd, posix=os.name != "nt")
    except ValueError as e:
        raise ValueError(f"Failed to parse command: {e}") from e

    # Validate each token against the approved list.
    for token in tokens:
        if token not in approved_subcommands:
            raise ValueError(f"Command '{token}' is not allowed")

    # Execute the command without using a shell.
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        # Return stderr if the command fails.
        return f"Command failed: {e.stderr.strip()}"
    except Exception as e:
        # Catch any other unexpected errors.
        return f"Execution error: {str(e)}"

    return result.stdout.strip()