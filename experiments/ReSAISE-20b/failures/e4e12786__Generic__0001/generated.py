import subprocess
import shutil
from typing import List

def execute_shell_command(command: str, args: List[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    command : str
        The base command to execute (e.g., "ls", "git").
    args : list
        A list of arguments for the command.

    Returns
    -------
    str
        The standard output from the executed command.

    Raises
    ------
    ValueError
        If the command is not found or execution fails.
    """
    # Ensure the base command exists in PATH
    if shutil.which(command) is None:
        raise ValueError(f"Command '{command}' not found or is not executable.")

    # Build the full command list
    cmd = [command] + args

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True  # Raises CalledProcessError on non-zero exit
        )
    except subprocess.CalledProcessError as e:
        raise ValueError(
            f"Command '{command}' failed with exit code {e.returncode}.\n"
            f"Stderr: {e.stderr.strip()}"
        ) from e
    except OSError as e:
        raise ValueError(f"Execution failed: {e}") from e

    return result.stdout.strip()