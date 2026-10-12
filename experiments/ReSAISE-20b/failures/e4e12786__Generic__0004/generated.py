import subprocess
import shlex
import shutil
from typing import List


def execute_shell_command(command: str, args: List[str]) -> str:
    """
    Execute a shell command with the supplied arguments and return its output.

    Parameters
    ----------
    command : str
        The base command to execute (e.g., "ls", "echo").
    args : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded stdout (and stderr if `stderr` is redirected to stdout) of the command.

    Raises
    ------
    ValueError
        If the command is not found or cannot be executed.
    """
    # Ensure the base command exists in PATH
    cmd_path = shutil.which(command)
    if not cmd_path:
        raise ValueError(f"Command '{command}' not found in PATH")

    # Build the command list. Using shlex.quote for safety is unnecessary
    # because we are not invoking a shell; however, it helps to ensure that
    # any special characters in args are treated literally.
    cmd = [cmd_path] + [shlex.quote(arg) for arg in args]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,  # we handle errors ourselves
        )
    except OSError as exc:
        raise ValueError(f"Failed to execute command '{command}': {exc}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{command}' exited with status {result.returncode}: "
            f"{result.stderr.strip()}"
        )

    return result.stdout