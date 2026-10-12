import subprocess
import shlex
import shutil
from typing import List


def run_shell_cmd(cmd_name: str, cmd_args: List[str]) -> str:
    """
    Execute a shell command with the supplied arguments and return its output.

    Parameters
    ----------
    cmd_name : str
        The main command to run (e.g., "ls", "grep").
    cmd_args : List[str]
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
    # Ensure the command exists and is executable
    full_path = shutil.which(cmd_name)
    if not full_path:
        raise ValueError(f"Command '{cmd_name}' not found in PATH")

    # Build the command list safely
    cmd_list = [full_path] + cmd_args

    try:
        # Execute the command
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            check=False,  # We'll handle errors ourselves
        )
    except Exception as exc:
        raise ValueError(f"Failed to execute command '{cmd_name}': {exc}") from exc

    # If the command failed (non-zero exit), raise ValueError
    if result.returncode != 0:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command '{cmd_name}' failed with exit code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    # Return stdout (and optionally stderr if needed)
    return result.stdout