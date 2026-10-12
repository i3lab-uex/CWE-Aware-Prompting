import os
import shlex
import subprocess
from typing import List

def filtered_system_command(cmd: str, approved_cmd_list: List[str]) -> str:
    """
    Execute a user supplied command only if every token in the command
    is present in ``approved_cmd_list``.  The function uses a safe
    invocation (no shell) to avoid injection and returns the command's
    output or an error message.

    Parameters
    ----------
    cmd : str
        The command string supplied by the user.
    approved_cmd_list : List[str]
        A list of tokens that are allowed to appear in the command.

    Returns
    -------
    str
        The combined stdout and stderr of the executed command, or an error
        message if execution failed.

    Raises
    ------
    ValueError
        If the command is empty or any token in ``cmd`` is not in
        ``approved_cmd_list``.
    """
    if not cmd or not cmd.strip():
        raise ValueError("Command must be a non‑empty string")

    # Tokenise the command safely
    try:
        tokens = shlex.split(cmd)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    # Ensure all tokens are approved
    for token in tokens:
        if token not in approved_cmd_list:
            raise ValueError(f"Token '{token}' is not allowed")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # We handle non‑zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        return f"Command not found: {exc}"
    except PermissionError as exc:
        return f"Permission denied: {exc}"
    except Exception as exc:
        return f"Execution failed: {exc}"

    # Return stdout and stderr together
    output = result.stdout + result.stderr

    if result.returncode != 0:
        output += f"\nCommand exited with status {result.returncode}"

    return output