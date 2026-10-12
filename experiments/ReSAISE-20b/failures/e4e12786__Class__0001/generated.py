import subprocess
import shutil
from typing import List

def execute_shell_command(command: str, args: List[str]) -> str:
    """
    Execute a shell command with the given arguments safely.

    Parameters
    ----------
    command : str
        The base executable to run (e.g., "ls", "python").
    args : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The combined stdout and stderr output of the executed command.

    Raises
    ------
    ValueError
        If the command is not found, or if execution fails.
    """
    # Ensure the base command exists in PATH
    executable = shutil.which(command)
    if not executable:
        raise ValueError(f"Command '{command}' not found in PATH")

    # Build the full command list
    cmd = [executable] + args

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False  # We handle non-zero exit manually
        )
    except OSError as exc:
        raise ValueError(f"Failed to execute command '{command}': {exc}") from exc

    # Combine stdout and stderr for consistency
    output = result.stdout + result.stderr

    if result.returncode != 0:
        raise ValueError(
            f"Command '{command}' exited with status {result.returncode}\n"
            f"Output: {output}"
        )

    return output