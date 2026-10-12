import subprocess
import shutil
from typing import List

def execute_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    cmd : str
        The command to execute. Must be a valid executable name or path.
    arguments : List[str]
        A list of string arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be found or fails to execute.
    """
    # Ensure the command is available on the system path
    cmd_path = shutil.which(cmd)
    if not cmd_path:
        raise ValueError(f"Command '{cmd}' not found or is not executable.")

    # Build the full argument list
    exec_args = [cmd_path] + arguments

    try:
        result = subprocess.run(
            exec_args,
            capture_output=True,
            text=True,          # decode bytes to str automatically
            check=True          # raise CalledProcessError on non-zero exit
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command '{cmd}' not found.") from e
    except subprocess.CalledProcessError as e:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command '{cmd}' failed with exit code {e.returncode}:\n{e.stderr}"
        ) from e
    except Exception as e:
        raise ValueError(f"Failed to execute command '{cmd}': {e}") from e

    return result.stdout