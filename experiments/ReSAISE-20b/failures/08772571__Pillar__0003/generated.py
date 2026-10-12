import subprocess
from typing import List


def call_system_command(sys_command: str, params: List[str]) -> str:
    """
    Execute a system command with the supplied arguments and return its output.

    Parameters
    ----------
    sys_command : str
        The base command to run (e.g., "ls", "git").
    params : list[str]
        A list of arguments for the command.

    Returns
    -------
    str
        The decoded standard output from the executed command.

    Raises
    ------
    ValueError
        If the command is empty, contains non-string arguments, or fails to execute.
    """
    # Basic validation – ensure command is a string and not empty
    if not isinstance(sys_command, str) or not sys_command.strip():
        raise ValueError("sys_command must be a non‑empty string")

    # Ensure params is a list of strings
    if not isinstance(params, list):
        raise ValueError("params must be a list")
    for i, p in enumerate(params):
        if not isinstance(p, str):
            raise ValueError(f"param at index {i} is not a string")

    # Construct the argument list for subprocess
    cmd = [sys_command] + params

    try:
        # Run the command without invoking a shell for security
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,           # decode bytes to str using locale encoding
            check=True,          # raise CalledProcessError on non‑zero exit
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {sys_command}") from exc
    except subprocess.CalledProcessError as exc:
        # Include stdout/stderr in the error message for debugging
        raise ValueError(
            f"Command failed with exit code {exc.returncode}:\n"
            f"stdout: {exc.stdout}\nstderr: {exc.stderr}"
        ) from exc
    except Exception as exc:
        raise ValueError(f"Unexpected error executing command: {exc}") from exc

    return result.stdout