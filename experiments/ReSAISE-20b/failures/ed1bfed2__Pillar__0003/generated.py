import shlex
import subprocess
from typing import List


def run_shell_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the given list of arguments and return its stdout.

    Parameters
    ----------
    cmd : str
        The primary command to run. May contain whitespace; it will be split safely.
    arguments : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command is empty, if the process exits with a non‑zero status,
        or if an unexpected exception occurs during execution.
    """
    # Basic validation
    if not isinstance(cmd, str) or not cmd.strip():
        raise ValueError("The base command must be a non‑empty string.")

    if not isinstance(arguments, list):
        raise ValueError("Arguments must be provided as a list.")

    # Split the command safely and combine with arguments
    try:
        base_cmd_parts = shlex.split(cmd, posix=True)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    # Ensure the first part is a valid executable
    if not base_cmd_parts:
        raise ValueError("Command resolution failed: no executable found.")

    # Construct the full command list
    cmd_list = base_cmd_parts + arguments

    try:
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            check=False,  # we handle errors manually
        )
    except OSError as exc:
        raise ValueError(f"Execution failed: {exc}") from exc

    if result.returncode != 0:
        err_msg = (
            f"Command '{cmd}' failed with exit code {result.returncode}.\n"
            f"stderr: {result.stderr.strip()}"
        )
        raise ValueError(err_msg)

    return result.stdout