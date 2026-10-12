import os
import shlex
import subprocess
from typing import List


def execute_command_with_restrictions(
    cmd: str, approved_subcommands: List[str]
) -> str:
    """
    Execute a shell command only if it contains approved subcommands.

    Parameters
    ----------
    cmd : str
        The command to execute.
    approved_subcommands : list[str]
        A list of subcommand names that are allowed.

    Returns
    -------
    str
        The stdout from the executed command if it is allowed,
        otherwise an error message.

    Raises
    ------
    ValueError
        If the command is empty or any token in it is not in
        `approved_subcommands`.
    """
    if not cmd.strip():
        raise ValueError("Empty command is not allowed")

    # Split the command into arguments safely
    try:
        parts = shlex.split(cmd)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    # Validate each subcommand (token) against the approved list
    for token in parts:
        if token not in approved_subcommands:
            raise ValueError(
                f"Subcommand '{token}' is not permitted. Allowed: {approved_subcommands}"
            )

    # Execute the command safely using subprocess
    try:
        result = subprocess.run(
            parts,
            capture_output=True,
            text=True,
            check=False,  # We'll handle non-zero exit ourselves
        )
    except Exception as exc:
        return f"Execution failed: {exc}"

    if result.returncode != 0:
        return (
            f"Command exited with code {result.returncode}.\n"
            f"stderr: {result.stderr.strip()}"
        )

    return result.stdout