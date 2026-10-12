import os
import shlex
import subprocess
from typing import List

def execute_permitted_command(input_command: str, approved_commands: List[str]) -> str:
    """
    Execute a shell command only if all non-option tokens are in the approved list.

    Parameters
    ----------
    input_command : str
        The user supplied command string.
    approved_commands : list[str]
        List of permitted subcommands / tokens.

    Returns
    -------
    str
        Combined stdout and stderr from the executed command, or an error message.

    Raises
    ------
    ValueError
        If any non-option token in the command is not present in ``approved_commands``.
    """
    # Tokenize respecting quotes, etc.
    tokens = shlex.split(input_command)

    if not tokens:
        raise ValueError("Empty command is not allowed")

    # Validate each non-option token
    for token in tokens:
        if token.startswith('-'):
            continue  # ignore options
        if token not in approved_commands:
            raise ValueError(f"Command '{token}' is not permitted")

    # Use subprocess.run to execute the command safely
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # we handle errors ourselves
        )
    except FileNotFoundError as exc:
        return f"Command not found: {exc}"
    except Exception as exc:
        return f"Execution failed: {exc}"

    output = result.stdout + result.stderr
    if not output:
        output = f"Command executed with exit code {result.returncode}, but produced no output."
    return output