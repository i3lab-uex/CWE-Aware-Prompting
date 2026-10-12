import subprocess
import shlex
import shutil
from typing import List

def run_shell_cmd(cmd: str, params: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    cmd : str
        The executable command to run.
    params : list of str
        List of arguments passed to the command.

    Returns
    -------
    str
        Decoded standard output from the executed command.

    Raises
    ------
    ValueError
        If the command is not found, cannot be executed, or returns a non‑zero exit status.
    """
    # Ensure the command exists on the system
    if not shutil.which(cmd):
        raise ValueError(f"Command '{cmd}' not found or is not executable.")

    # Build the argument list: first element is command, followed by params
    cmd_list = [cmd] + params

    try:
        # Run the command without invoking a shell to avoid injection risks
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,          # returns str instead of bytes
            check=True          # raise CalledProcessError on non-zero exit
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command '{cmd}' could not be found: {e}") from e
    except subprocess.CalledProcessError as e:
        # Include stdout/stderr in the error message for debugging
        msg = (
            f"Command '{cmd}' failed with exit code {e.returncode}.\n"
            f"Stdout: {e.stdout}\nStderr: {e.stderr}"
        )
        raise ValueError(msg) from e
    except Exception as e:
        # Catch any other unexpected exceptions and wrap them in ValueError
        raise ValueError(f"Unexpected error while running '{cmd}': {e}") from e

    return result.stdout