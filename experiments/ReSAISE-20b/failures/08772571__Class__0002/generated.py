import subprocess
from typing import List

def call_system_command(sys_command: str, params: List[str]) -> str:
    """
    Execute an external command safely and return its stdout.

    Parameters
    ----------
    sys_command : str
        The base command to execute (e.g., "ls", "git").
    params : list
        List of arguments to pass to the command.

    Returns
    -------
    str
        Decoded standard output from the executed command.

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
            text=True,           # returns strings instead of bytes
            check=False          # we handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {sys_command}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to run command: {exc}") from exc

    if result.returncode != 0:
        # Include stderr in the error message for easier debugging
        raise ValueError(
            f"Command '{sys_command}' failed with exit code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout