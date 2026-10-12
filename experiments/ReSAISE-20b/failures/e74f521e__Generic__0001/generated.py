import subprocess
import shlex
from typing import List


def run_shell_cmd(cmd: str, params: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    cmd : str
        The base command to run (e.g., 'ls', 'grep').
    params : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output of the executed command.

    Raises
    ------
    ValueError
        If the command cannot be found, is invalid, or execution fails.
    """
    # Build the argument list safely
    if not isinstance(cmd, str):
        raise ValueError("Command must be a string")
    if not isinstance(params, list) or any(not isinstance(p, str) for p in params):
        raise ValueError("Params must be a list of strings")

    # Construct the full command as a list for subprocess
    cmd_list = [cmd] + params

    try:
        # Run the command without invoking a shell for security
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,          # returns strings instead of bytes
            check=True,         # raise CalledProcessError on non-zero exit
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {cmd}") from e
    except subprocess.CalledProcessError as e:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command '{cmd}' failed with exit code {e.returncode}:\n{e.stderr}"
        ) from e
    except Exception as e:
        # Catch-all for unexpected errors
        raise ValueError(f"Failed to execute command '{cmd}': {e}") from e

    return result.stdout