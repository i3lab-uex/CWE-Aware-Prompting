import os
import shlex
import subprocess
from typing import List


def execute_permitted_command(input_command: str, approved_commands: List[str]) -> str:
    """
    Execute a shell command only if all of its tokens are present in the
    approved_commands list.

    Parameters
    ----------
    input_command : str
        The full command string supplied by the user.
    approved_commands : list[str]
        A list of permitted subcommands. Each token in the input command
        must be present in this list.

    Returns
    -------
    str
        The stdout of the executed command. If the command fails, the
        stderr will be returned instead.

    Raises
    ------
    ValueError
        If any token in the command is not found in `approved_commands`.
    """
    # Tokenise the command safely
    tokens = shlex.split(input_command)

    if not tokens:
        raise ValueError("Empty command")

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
            check=False,   # We handle non‑zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        return f"Command not found: {exc}"
    except PermissionError as exc:
        return f"Permission denied: {exc}"

    # Prefer stdout, but fall back to stderr if the command failed
    return result.stdout.strip() or result.stderr.strip()