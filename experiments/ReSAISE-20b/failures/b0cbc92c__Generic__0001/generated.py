import subprocess
import shlex
from typing import List


def run_command(cmd: str, cmd_arguments: List[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    cmd : str
        The main command to execute (e.g., "ls", "git").
    cmd_arguments : list
        A list of string arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If `cmd` is empty, if arguments are not a list of strings,
        or if the command fails to execute.
    """
    # Basic validation
    if not isinstance(cmd, str) or not cmd.strip():
        raise ValueError("Command must be a non-empty string.")
    if not isinstance(cmd_arguments, list) or any(
        not isinstance(arg, str) for arg in cmd_arguments
    ):
        raise ValueError("cmd_arguments must be a list of strings.")

    # Build the full command as a list; this avoids shell injection
    full_cmd = [cmd] + cmd_arguments

    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            check=False,  # We'll handle errors manually
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {cmd}") from e
    except Exception as e:
        raise ValueError(f"Failed to execute command: {cmd}") from e

    # If the process exited with a non-zero status, raise an error
    if result.returncode != 0:
        err_msg = (
            f"Command '{cmd}' failed with return code {result.returncode}.\n"
            f"Stderr: {result.stderr.strip()}"
        )
        raise ValueError(err_msg)

    return result.stdout