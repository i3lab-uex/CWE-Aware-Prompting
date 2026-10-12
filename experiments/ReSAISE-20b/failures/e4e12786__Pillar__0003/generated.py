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
        The base executable to run (e.g., "ls", "git").
    args : list[str]
        List of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output of the executed command.

    Raises
    ------
    ValueError
        If the command is empty, not found in PATH, or execution fails.
    """
    if not isinstance(command, str) or not command.strip():
        raise ValueError("Command must be a non-empty string")

    # Ensure the command exists in PATH
    executable = shutil.which(command)
    if not executable:
        raise ValueError(f"Command '{command}' not found in PATH")

    # Build the full command list
    cmd_list = [executable] + args

    try:
        # Execute without invoking the shell to avoid injection issues
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            check=False,  # we handle non-zero exit codes ourselves
        )
    except OSError as exc:
        raise ValueError(f"Execution failed: {exc}") from exc

    # Raise if the command returned a non-zero exit status
    if result.returncode != 0:
        raise ValueError(
            f"Command '{command}' failed with exit code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout