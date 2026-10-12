import os
import shlex
import subprocess
from typing import List

def execute_permitted_command(input_command: str, approved_commands: List[str]) -> str:
    """
    Execute a shell command only if all tokens are in the approved list.

    Parameters
    ----------
    input_command : str
        The full command string supplied by the user.
    approved_commands : list[str]
        A collection of permitted subcommands (tokens) that may be used.

    Returns
    -------
    str
        The combined stdout and stderr from the executed command.

    Raises
    ------
    ValueError
        If any token in the parsed command is not present in approved_commands.
    RuntimeError
        If the command fails to execute for reasons other than disallowed tokens.
    """
    # Tokenize the input while respecting quoting
    try:
        tokens = shlex.split(input_command)
    except ValueError as exc:
        raise RuntimeError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command is not allowed.")

    # Verify each token against the approved list
    for token in tokens:
        if token not in approved_commands:
            raise ValueError(f"Disallowed command component: '{token}'")

    # Execute the command safely
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # We'll handle non-zero exit codes manually
        )
    except OSError as exc:
        raise RuntimeError(f"Failed to execute command: {exc}") from exc

    # Combine stdout and stderr for simplicity
    output = result.stdout + result.stderr

    if result.returncode != 0:
        # Optionally, you can raise an exception here instead of returning output
        output += f"\nCommand exited with status {result.returncode}"

    return output