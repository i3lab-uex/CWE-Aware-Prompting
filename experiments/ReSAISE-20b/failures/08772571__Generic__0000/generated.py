import subprocess
import shlex
from typing import List


def call_system_command(sys_command: str, params: List[str]) -> str:
    """
    Execute an external command with the given arguments and return its output.

    Parameters
    ----------
    sys_command : str
        The command to execute (e.g., "ls", "git").
    params : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The stdout produced by the command.

    Raises
    ------
    ValueError
        If the command is invalid, fails to execute, or returns a non‑zero exit status.
    """
    if not isinstance(sys_command, str) or not sys_command:
        raise ValueError("`sys_command` must be a non‑empty string.")

    if not isinstance(params, list) or any(
        not isinstance(p, str) for p in params
    ):
        raise ValueError("`params` must be a list of strings.")

    # Construct the argument list safely
    cmd = [sys_command] + params

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,          # We handle non‑zero exit ourselves
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {sys_command}") from e
    except Exception as e:
        raise ValueError(f"Failed to execute command: {sys_command}") from e

    if result.returncode != 0:
        # Include both stdout and stderr in the error message
        err_msg = result.stderr.strip() or "Unknown error"
        raise ValueError(
            f"Command '{sys_command}' failed with exit code {result.returncode}: {err_msg}"
        )

    return result.stdout.strip()