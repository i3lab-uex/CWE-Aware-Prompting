import subprocess
import shlex
import shutil
from typing import List

def run_shell_cmd(cmd_name: str, cmd_args: List[str]) -> str:
    """
    Execute a shell command safely and return its output.

    Parameters
    ----------
    cmd_name : str
        The main command to run (e.g., 'ls', 'git').
    cmd_args : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output of the executed command.

    Raises
    ------
    ValueError
        If the command cannot be found, if arguments are invalid,
        or if the subprocess fails to execute successfully.
    """
    # Ensure cmd_name is a valid executable in PATH
    if not shutil.which(cmd_name):
        raise ValueError(f"Command '{cmd_name}' not found in PATH.")

    # Validate that cmd_args is a list of strings
    if not isinstance(cmd_args, list) or not all(isinstance(arg, str) for arg in cmd_args):
        raise ValueError("cmd_args must be a list of strings.")

    # Construct the full command as a list; no shell=True to avoid injection
    full_cmd = [cmd_name] + cmd_args

    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,          # Decode bytes to str automatically
            check=True,         # Raise CalledProcessError on non-zero exit
        )
    except subprocess.CalledProcessError as e:
        # Include stdout/stderr in the error message for debugging
        msg = (
            f"Command '{cmd_name}' failed with exit code {e.returncode}.\n"
            f"Stdout: {e.stdout}\nStderr: {e.stderr}"
        )
        raise ValueError(msg) from e
    except OSError as e:
        # Handle errors like permission denied, etc.
        raise ValueError(f"Execution failed: {e}") from e

    return result.stdout