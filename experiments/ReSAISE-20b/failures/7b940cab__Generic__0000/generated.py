import subprocess
import shlex
from typing import List


def execute_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the supplied arguments and return its output.

    Parameters
    ----------
    cmd : str
        The command to run (may contain spaces or shell operators).
    arguments : list[str]
        List of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed or returns a non‑zero exit status.
    """
    # Safely split the command string into tokens
    try:
        base_cmd = shlex.split(cmd)
    except ValueError as exc:  # shlex can raise ValueError on bad input
        raise ValueError(f"Invalid command string: {cmd!r}") from exc

    # Build the full argument list
    full_cmd = base_cmd + arguments

    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,          # decode bytes to str using locale encoding
            check=False,        # we will handle non‑zero exit ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {base_cmd[0]!r}") from exc
    except OSError as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command exited with status {result.returncode}: "
            f"{result.stderr.strip() or 'no error message'}"
        )

    return result.stdout