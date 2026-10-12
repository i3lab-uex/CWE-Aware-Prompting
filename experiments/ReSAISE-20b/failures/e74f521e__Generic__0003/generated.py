import subprocess
import shlex
from typing import List

def run_shell_cmd(cmd: str, params: List[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    cmd : str
        The base command to execute (e.g., "ls", "grep").
    params : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output from the executed command.

    Raises
    ------
    ValueError
        If the command is empty, not a string, or execution fails.
    """
    if not isinstance(cmd, str) or not cmd.strip():
        raise ValueError("Command must be a non-empty string")

    if not isinstance(params, list):
        raise ValueError("Params must be a list of strings")

    # Build the command line safely
    try:
        cmd_list = [cmd] + params
        # Ensure each element is a string; shlex.split is not needed here because we build the list manually
    except Exception as exc:
        raise ValueError(f"Failed to construct command: {exc}") from exc

    try:
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as exc:
        # Provide detailed error information
        raise ValueError(
            f"Command '{cmd}' failed with exit code {exc.returncode}:\n"
            f"Stdout: {exc.stdout}\nStderr: {exc.stderr}"
        ) from exc
    except FileNotFoundError as exc:
        raise ValueError(f"Command '{cmd}' not found") from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command '{cmd}': {exc}") from exc

    return result.stdout