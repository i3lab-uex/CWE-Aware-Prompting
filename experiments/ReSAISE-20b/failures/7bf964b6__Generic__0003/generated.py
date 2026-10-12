import os
import shlex
import subprocess
from typing import List


def validate_and_execute_command(shell_cmd: str, safe_subcommands: List[str]) -> str:
    """
    Execute a shell command only if all tokens are in the allowed list.

    Parameters
    ----------
    shell_cmd : str
        The command to execute.
    safe_subcommands : list[str]
        A list of permitted subcommand tokens.

    Returns
    -------
    str
        The command's stdout if executed successfully, or an error message.

    Raises
    ------
    ValueError
        If any token in the command is not in `safe_subcommands`.
    """
    # Split the command into tokens safely
    try:
        tokens = shlex.split(shell_cmd)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    # Validate each token against the safe list
    for token in tokens:
        if token not in safe_subcommands:
            raise ValueError(f"Command '{token}' is not allowed.")

    # Execute the command
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # We handle non-zero exit ourselves
        )
    except OSError as exc:
        return f"Execution failed: {exc}"

    if result.returncode != 0:
        # Return the stderr as error output
        return f"Command failed with exit {result.returncode}:\n{result.stderr}"
    return result.stdout