import subprocess
import shlex
from shutil import which
from typing import List


def run_shell_cmd(cmd_name: str, cmd_args: List[str]) -> str:
    """
    Execute a shell command safely and return its output.

    Parameters
    ----------
    cmd_name : str
        The main command to execute (e.g., 'ls', 'git').
    cmd_args : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output from the executed command.

    Raises
    ------
    ValueError
        If the command is not found, if arguments are of wrong type,
        or if the command exits with a non‑zero status.
    """
    # Basic input validation
    if not isinstance(cmd_name, str) or not cmd_name:
        raise ValueError("cmd_name must be a non-empty string")

    if not isinstance(cmd_args, list):
        raise ValueError("cmd_args must be a list of strings")

    for arg in cmd_args:
        if not isinstance(arg, str):
            raise ValueError("All items in cmd_args must be strings")

    # Ensure the command exists on the system
    if which(cmd_name) is None:
        raise ValueError(f"Command '{cmd_name}' not found in PATH")

    # Build the command list for subprocess (no shell expansion)
    full_cmd = [cmd_name] + cmd_args

    try:
        result = subprocess.run(
            full_cmd,
            check=True,                 # Raise CalledProcessError on non-zero exit
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,   # Combine stdout and stderr for easier debugging
            text=True,                  # Decode bytes to str using default encoding (utf-8)
        )
    except subprocess.CalledProcessError as exc:
        # Provide a clear error message including the command that failed
        raise ValueError(
            f"Command '{cmd_name}' failed with exit code {exc.returncode}.\n"
            f"Output:\n{exc.output}"
        ) from exc

    return result.stdout