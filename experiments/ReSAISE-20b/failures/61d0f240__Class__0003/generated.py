import os
import shlex
import subprocess
from typing import List


def execute_permitted_command(input_command: str, approved_commands: List[str]) -> str:
    """
    Execute a shell command only if every token is in the approved_commands list.

    Parameters
    ----------
    input_command : str
        The user-supplied command string.
    approved_commands : List[str]
        A list of allowed subcommands or arguments.

    Returns
    -------
    str
        The standard output from the executed command, decoded as UTF-8.
        If an error occurs during execution, its stderr is returned.

    Raises
    ------
    ValueError
        If any token in the command is not present in approved_commands.
    """
    # Split the command into tokens safely
    try:
        tokens = shlex.split(input_command)
    except ValueError as exc:  # malformed command
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command")

    # Verify that every token is approved
    for token in tokens:
        if token not in approved_commands:
            raise ValueError(f"Disallowed command part: '{token}'")

    # Execute the command without invoking a shell to avoid injection
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # we handle non-zero exit ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {tokens[0]}") from exc
    except Exception as exc:
        raise ValueError(f"Execution failed: {exc}") from exc

    # Return stdout or stderr based on exit status
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        # Include stderr for debugging but avoid leaking sensitive data
        return result.stderr.strip()