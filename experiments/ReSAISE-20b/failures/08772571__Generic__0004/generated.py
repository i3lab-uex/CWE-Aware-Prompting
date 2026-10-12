import subprocess
import shlex
from typing import List


def call_system_command(sys_command: str, params: List[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    sys_command : str
        The base command to run (e.g., "ls", "grep").
    params : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output of the executed command.

    Raises
    ------
    ValueError
        If the command is not found or returns a non‑zero exit status.
    """
    # Build the full argument list, ensuring each param is safely quoted
    cmd = [sys_command] + params

    try:
        # Run the command without invoking a shell for safety
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,  # we will handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {sys_command}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command: {sys_command}") from exc

    if result.returncode != 0:
        err_msg = (
            f"Command '{shlex.join(cmd)}' failed with exit code "
            f"{result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"
        )
        raise ValueError(err_msg)

    return result.stdout