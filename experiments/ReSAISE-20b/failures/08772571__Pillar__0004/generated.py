import subprocess
import shlex
from typing import List


def call_system_command(sys_command: str, params: List[str]) -> str:
    """
    Execute a system command with the given arguments and return its stdout.

    Parameters
    ----------
    sys_command : str
        The base command to execute (e.g., 'ls', 'grep').
    params : list
        A list of string arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output of the executed command.

    Raises
    ------
    ValueError
        If the command cannot be found, fails to execute, or returns a non‑zero exit code.
    """
    # Build the argument list for subprocess (no shell usage)
    try:
        command = [sys_command] + params
        # Ensure all arguments are strings and properly escaped for the shell
        command = [str(arg) for arg in command]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,  # decode output using locale encoding
            check=False,  # we handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {sys_command}") from exc
    except OSError as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        # Combine stderr and stdout for debugging
        error_msg = (
            f"Command '{sys_command}' failed with exit code {result.returncode}.\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )
        raise ValueError(error_msg)

    return result.stdout