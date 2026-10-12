import os
import shlex
import subprocess
from typing import List


def filtered_system_command(cmd: str, approved_cmd_list: List[str]) -> str:
    """
    Execute a shell command after validating that every token is in the approved list.

    Parameters
    ----------
    cmd : str
        The user‑supplied command string.
    approved_cmd_list : list[str]
        List of subcommands that are allowed to be executed.

    Returns
    -------
    str
        Standard output and standard error of the command, or an error message.

    Raises
    ------
    ValueError
        If any token in the command is not present in `approved_cmd_list`.
    """
    # Tokenise the command safely (no shell interpretation)
    try:
        tokens = shlex.split(cmd, posix=True)
    except ValueError as exc:
        return f"Command parsing error: {exc}"

    if not tokens:
        return "No command provided."

    # Validate each token
    for token in tokens:
        if token not in approved_cmd_list:
            raise ValueError(f"Disallowed command component: {token!r}")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,   # We'll handle non‑zero exit codes ourselves
        )
    except FileNotFoundError:
        return f"Command not found: {tokens[0]!r}"
    except Exception as exc:
        return f"Execution error: {exc}"

    # Combine stdout and stderr for the caller
    output = result.stdout + result.stderr

    if result.returncode != 0:
        output += f"\nCommand exited with return code {result.returncode}"
    return output