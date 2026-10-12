import subprocess
import shlex
from shutil import which
from pathlib import Path

def call_system_command(sys_command: str, params: list) -> str:
    """
    Execute a system command with the given arguments and return its output.

    Parameters
    ----------
    sys_command : str
        The base command to run (e.g., "ls", "/usr/bin/echo").
    params : list
        A list of string arguments to pass to the command.

    Returns
    -------
    str
        The combined standard output and standard error from the executed command.

    Raises
    ------
    ValueError
        If `sys_command` is not a valid executable or the command exits with a non‑zero status.
    """
    if not isinstance(sys_command, str):
        raise ValueError("sys_command must be a string")

    # Resolve the command to an absolute path if possible
    cmd_path = which(sys_command)
    if cmd_path is None:
        # It might be a script or binary in the current directory
        if not Path(sys_command).is_file():
            raise ValueError(f"Command '{sys_command}' not found")
        cmd_path = sys_command

    # Ensure all params are strings
    if not all(isinstance(p, str) for p in params):
        raise ValueError("All parameters must be strings")

    # Build the argument list
    args = [cmd_path] + params

    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False  # We'll handle errors ourselves
        )
    except OSError as exc:
        raise ValueError(f"Failed to execute '{sys_command}': {exc}") from exc

    output = result.stdout + result.stderr
    if result.returncode != 0:
        raise ValueError(
            f"Command '{sys_command}' failed with exit code {result.returncode}:\n{output}"
        )

    return output