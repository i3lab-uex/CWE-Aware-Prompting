import subprocess
import shlex
from typing import List


def call_system_command(sys_command: str, params: List[str]) -> str:
    """
    Execute a system command with the given arguments and return its output.

    Parameters
    ----------
    sys_command : str
        The base command to run (e.g., "ls", "git").
    params : list
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The combined stdout and stderr output of the command.

    Raises
    ------
    ValueError
        If the command cannot be executed or returns a non‑zero exit status.
    """
    # Build the full argument list safely
    command = [sys_command] + params

    try:
        # Execute without using the shell to avoid injection risks
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,  # We'll handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {sys_command}") from exc
    except OSError as exc:
        raise ValueError(f"Execution failed for command: {sys_command}") from exc

    # If the process exited with an error, raise ValueError
    if result.returncode != 0:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command '{sys_command}' failed with exit code {result.returncode}:\n"
            f"{result.stderr}"
        )

    # Return the captured output (stdout + stderr if needed)
    return result.stdout