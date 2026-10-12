import subprocess
from typing import List

def call_system_command(sys_command: str, params: List[str]) -> str:
    """
    Execute an external command safely and return its output.

    Parameters
    ----------
    sys_command : str
        The base command to execute (e.g., "ls", "/usr/bin/python").
    params : list
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The combined standard output and standard error from the executed command.

    Raises
    ------
    ValueError
        If the command fails to execute or returns a non‑zero exit status.
    """
    # Build the argument list for subprocess.run
    cmd = [sys_command] + params

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False  # We'll handle non‑zero exit status ourselves
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {sys_command}") from e
    except OSError as e:
        raise ValueError(f"Execution failed: {e}") from e

    # Combine stdout and stderr for the return value
    output = result.stdout + result.stderr

    if result.returncode != 0:
        raise ValueError(
            f"Command '{sys_command}' failed with exit code {result.returncode}:\n{output}"
        )

    return output