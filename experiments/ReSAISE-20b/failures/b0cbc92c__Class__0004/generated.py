import subprocess
import shlex
import shutil
from typing import List

def run_command(cmd: str, cmd_arguments: List[str]) -> str:
    """
    Execute a shell command safely and return its output.

    Parameters
    ----------
    cmd : str
        The base command to execute (e.g., 'ls', 'grep').
    cmd_arguments : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The combined stdout and stderr produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be found, or if execution fails.
    """
    # Ensure the base command exists on the system
    cmd_path = shutil.which(cmd)
    if not cmd_path:
        raise ValueError(f"Command '{cmd}' not found in PATH")

    # Build the argument list: first element is the command path
    args = [cmd_path] + cmd_arguments

    try:
        # Execute the command without using a shell to avoid injection
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False  # We handle errors manually
        )
    except OSError as e:
        raise ValueError(f"Execution failed for '{cmd}': {e}") from e

    # Combine stdout and stderr for a single string output
    output = result.stdout + result.stderr

    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd}' exited with code {result.returncode}.\n"
            f"Output:\n{output}"
        )

    return output