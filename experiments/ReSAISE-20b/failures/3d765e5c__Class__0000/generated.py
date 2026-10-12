import os
import shlex
import subprocess
from typing import List

def filtered_system_command(cmd: str, approved_cmd_list: List[str]) -> str:
    """
    Execute a user‑supplied shell command after verifying that every token
    is present in the approved_cmd_list.  The function uses a safe API
    (subprocess.run with shell=False) to avoid command‑injection attacks.

    Parameters
    ----------
    cmd : str
        The raw shell command supplied by the user.
    approved_cmd_list : List[str]
        A list of permitted sub‑commands or arguments.  Every token in
        `cmd` must be present here; otherwise a ValueError is raised.

    Returns
    -------
    str
        The standard output of the command if it runs successfully.
        If the command fails, the function returns the error message.

    Raises
    ------
    ValueError
        If any token in `cmd` is not found in `approved_cmd_list`.
    """
    # Tokenise the command safely
    try:
        tokens = shlex.split(cmd)
    except ValueError as exc:   # e.g. unmatched quotes
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command provided")

    # Verify each token against the approved list
    for token in tokens:
        if token not in approved_cmd_list:
            raise ValueError(f"Command or argument '{token}' is not allowed")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False  # We will handle non‑zero exit codes ourselves
        )
    except OSError as exc:
        # e.g. command not found, permission denied
        return f"Execution error: {exc}"

    # Return stdout or stderr depending on success
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Command failed (exit {result.returncode}): {result.stderr.strip()}"