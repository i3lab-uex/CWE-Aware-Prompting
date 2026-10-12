import os
import shlex
import subprocess
from typing import List

def execute_permitted_command(input_command: str, approved_commands: List[str]) -> str:
    """
    Execute a shell command only if every token in the command is present
    in ``approved_commands``.

    Parameters
    ----------
    input_command : str
        The user‑supplied command string.
    approved_commands : List[str]
        A list of allowed subcommands.  Each token in the command must match
        one of these exactly.

    Returns
    -------
    str
        The standard output of the command if it succeeds, otherwise an error
        message containing stderr.

    Raises
    ------
    ValueError
        If any token in the command is not present in ``approved_commands``.
    """
    # Tokenise the input safely (respecting quotes, escapes, etc.)
    try:
        tokens = shlex.split(input_command)
    except ValueError as exc:
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("No command provided")

    # Validate each token
    for token in tokens:
        if token not in approved_commands:
            raise ValueError(f"Command '{token}' is not permitted")

    # Execute the command
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # We handle errors ourselves
        )
    except OSError as exc:
        return f"Execution failed: {exc}"

    if result.returncode != 0:
        return f"Error ({result.returncode}): {result.stderr.strip()}"

    return result.stdout.strip()