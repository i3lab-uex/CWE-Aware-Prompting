import subprocess
import shutil
from typing import List


def run_shell_cmd(cmd_name: str, cmd_args: List[str]) -> str:
    """
    Execute a shell command safely and return its output.

    Parameters
    ----------
    cmd_name : str
        The main executable to run.
    cmd_args : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command is not found, cannot be executed, or returns a non‑zero exit status.
    """
    # Verify that the command exists and is executable
    if shutil.which(cmd_name) is None:
        raise ValueError(f"Command '{cmd_name}' not found or not executable")

    # Build the command list; no shell=True to avoid injection
    cmd = [cmd_name] + cmd_args

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False  # We'll handle errors manually
        )
    except OSError as exc:
        raise ValueError(f"Failed to execute command '{cmd_name}': {exc}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd_name}' exited with status {result.returncode}: "
            f"{result.stderr.strip()}"
        )

    return result.stdout