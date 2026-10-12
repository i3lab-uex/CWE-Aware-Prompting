import subprocess
from typing import List

def call_system_command(sys_command: str, params: List[str]) -> str:
    """
    Execute a shell command safely with the supplied arguments and return its output.

    Parameters
    ----------
    sys_command : str
        The base command to run (e.g., "ls", "git").
    params : list[str]
        A list of arguments to pass to the command. Each element must be a string.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command fails to execute, is not found, or returns a non‑zero exit status.
    """
    if not isinstance(sys_command, str):
        raise ValueError("sys_command must be a string")
    if not isinstance(params, list) or not all(isinstance(p, str) for p in params):
        raise ValueError("params must be a list of strings")

    # Construct the argument list for subprocess.run
    cmd = [sys_command] + params

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,          # decode bytes to str
            check=True,         # raise CalledProcessError on non‑zero exit status
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {sys_command}") from e
    except subprocess.CalledProcessError as e:
        # Include stdout and stderr in the error message for debugging
        msg = (
            f"Command '{sys_command}' failed with exit code {e.returncode}.\n"
            f"Stdout: {e.stdout}\nStderr: {e.stderr}"
        )
        raise ValueError(msg) from e
    except Exception as e:
        # Catch any other unexpected exceptions and wrap them
        raise ValueError(f"Failed to execute command '{sys_command}': {e}") from e

    return result.stdout