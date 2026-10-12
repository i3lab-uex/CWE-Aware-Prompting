import os
import shlex
import subprocess
from typing import List


def filtered_system_command(cmd: str, approved_cmd_list: List[str]) -> str:
    """
    Execute a user‑supplied shell command after verifying that every token
    (command and its arguments) is present in the list of approved subcommands.

    Parameters
    ----------
    cmd : str
        The full command string supplied by the user.
    approved_cmd_list : List[str]
        A list of allowed tokens. Each token in the command must appear
        verbatim in this list; otherwise a ValueError is raised.

    Returns
    -------
    str
        The combined stdout and stderr of the executed command, or an error
        message if execution fails.

    Raises
    ------
    ValueError
        If any token in the parsed command is not present in ``approved_cmd_list``.
    """
    if not cmd.strip():
        raise ValueError("Command string is empty")

    # Tokenize the command safely (no shell=True)
    try:
        tokens = shlex.split(cmd, posix=True)
    except ValueError as e:  # shlex can raise if quotes are unbalanced
        raise ValueError(f"Failed to parse command: {e}")

    # Verify each token against the approved list
    for token in tokens:
        if token not in approved_cmd_list:
            raise ValueError(f"Unauthorized subcommand or argument: {token!r}")

    # Execute the command securely
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # Don't raise on non‑zero exit status
        )
    except FileNotFoundError:
        return f"Command not found: {tokens[0]!r}"
    except Exception as exc:
        return f"Execution error: {exc}"

    # Combine stdout and stderr for the caller
    output = result.stdout + result.stderr

    return output.strip()