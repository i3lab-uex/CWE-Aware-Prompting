import subprocess
import shlex
import shutil
from typing import List


def call_system_command(sys_command: str, params: List[str]) -> str:
    """
    Execute an external command with the given parameters and return its output.

    Parameters
    ----------
    sys_command : str
        The primary command to run (e.g., 'ls', 'git', etc.).
    params : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command is not found or fails to execute.
    """
    # Ensure the base command exists in PATH
    if shutil.which(sys_command) is None:
        raise ValueError(f"Command not found: {shlex.quote(sys_command)}")

    # Build the argument list for subprocess.run
    command = [sys_command] + params

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,          # We will handle non-zero exit codes ourselves
        )
    except OSError as exc:
        raise ValueError(f"Failed to execute command {shlex.quote(sys_command)}: {exc}") from exc

    if result.returncode != 0:
        # Include stderr in the error message to aid debugging
        err_msg = result.stderr.strip() or "Unknown error"
        raise ValueError(
            f"Command {shlex.quote(sys_command)} exited with code "
            f"{result.returncode}: {err_msg}"
        )

    return result.stdout.strip()