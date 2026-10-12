import os
import shlex
import subprocess
from typing import List


def filtered_system_command(cmd: str, approved_cmd_list: List[str]) -> str:
    """
    Execute a system command after verifying that every token is in the approved list.

    Parameters
    ----------
    cmd : str
        The shell command supplied by the user.
    approved_cmd_list : list[str]
        A collection of permitted subcommands that may be executed.

    Returns
    -------
    str
        The combined stdout and stderr of the executed command.

    Raises
    ------
    ValueError
        If any token in the command is not present in `approved_cmd_list`.
    """
    # Tokenise the command safely
    try:
        tokens = shlex.split(cmd, posix=True)
    except ValueError as exc:  # malformed quoting
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command")

    # Ensure every token is approved
    for token in tokens:
        if token not in approved_cmd_list:
            raise ValueError(f"Command '{token}' is not allowed")

    # Execute the command securely (no shell)
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # we handle errors ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Executable not found: {exc}") from exc
    except Exception as exc:
        raise ValueError(f"Execution failed: {exc}") from exc

    # Return stdout + stderr for visibility
    output = result.stdout or ""
    error_output = result.stderr or ""

    return f"{output}{error_output}"