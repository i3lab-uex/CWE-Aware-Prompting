import subprocess
import shutil
from typing import List

def execute_shell_command(command: str, args: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its standard output.

    Parameters
    ----------
    command : str
        The base command to execute (e.g., "ls", "git").
    args : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command is not found, if any argument is not a string,
        or if the command exits with a non‑zero status.
    """
    # Validate that all arguments are strings
    if not isinstance(args, list) or any(not isinstance(arg, str) for arg in args):
        raise ValueError("All arguments must be a list of strings.")

    # Ensure the command exists in PATH
    cmd_path = shutil.which(command)
    if cmd_path is None:
        raise ValueError(f"Command '{command}' not found in PATH.")

    # Build the full command list
    cmd_list = [cmd_path] + args

    try:
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            check=False,  # We'll handle non‑zero status manually
        )
    except Exception as exc:
        raise ValueError(f"Failed to execute command '{command}': {exc}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{command}' exited with status {result.returncode}:\n{result.stderr}"
        )

    return result.stdout