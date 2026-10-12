import subprocess
import shlex
import shutil
from typing import List

def execute_shell_command(command: str, args: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    command : str
        The base command to execute (e.g., 'ls', 'git').
    args : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The combined stdout and stderr of the executed command as a string.

    Raises
    ------
    ValueError
        If the command is not found or cannot be executed.
    """
    # Ensure the command exists in the system path
    cmd_path = shutil.which(command)
    if not cmd_path:
        raise ValueError(f"Command '{command}' not found in PATH")

    # Build the full argument list
    # Avoid shell=True to mitigate command injection (CWE-77)
    cmd_list = [cmd_path] + args

    try:
        # Run the command, capture output and errors
        result = subprocess.run(
            cmd_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False  # We'll handle errors ourselves
        )
    except OSError as exc:
        raise ValueError(f"Failed to execute '{command}': {exc}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{command}' exited with code {result.returncode}:\n{result.stdout}"
        )

    return result.stdout