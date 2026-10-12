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
        The main command to execute (e.g., "ls", "grep").
    cmd_args : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command does not exist or execution fails.
    """
    # Ensure cmd_name is a valid executable
    if not shutil.which(cmd_name):
        raise ValueError(f"Command '{cmd_name}' not found or is not executable.")

    # Build the command list
    cmd = [cmd_name] + cmd_args

    try:
        # Run the command without invoking a shell for security
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
    except OSError as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    # Raise an error if the command exited with a non-zero status
    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd_name}' exited with code {result.returncode}.\n"
            f"stderr: {result.stderr.strip()}"
        )

    return result.stdout