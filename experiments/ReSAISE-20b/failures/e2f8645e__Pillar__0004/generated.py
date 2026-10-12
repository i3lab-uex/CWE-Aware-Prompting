import os
import shlex
import subprocess
from typing import List


def execute_command_with_restrictions(
    cmd: str,
    approved_subcommands: List[str]
) -> str:
    """
    Execute a shell command only if all subcommands are in the approved list.

    Parameters
    ----------
    cmd : str
        The command string to be executed.
    approved_subcommands : List[str]
        A list of subcommand names that are considered safe and permitted.

    Returns
    -------
    str
        The standard output of the executed command if successful,
        otherwise an error message indicating that the command was not allowed.

    Raises
    ------
    ValueError
        If the command or any of its subcommands are not in the approved list.
    """
    # Split the command safely
    try:
        parts = shlex.split(cmd)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not parts:
        raise ValueError("Empty command provided")

    # The first token is the executable; all tokens after that are considered subcommands
    # For stricter policy you could also check the executable itself.
    for token in parts[1:]:
        if token not in approved_subcommands:
            raise ValueError(
                f"Subcommand '{token}' is not permitted. Allowed subcommands: {approved_subcommands}"
            )

    # Execute the command safely
    try:
        result = subprocess.run(
            parts,
            capture_output=True,
            text=True,
            check=False,  # We handle non-zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Executable not found: {parts[0]}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        return (
            f"Command failed with exit code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout.strip()