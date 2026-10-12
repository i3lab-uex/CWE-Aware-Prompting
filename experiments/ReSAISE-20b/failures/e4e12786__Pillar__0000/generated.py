import subprocess
from typing import List


def execute_shell_command(command: str, args: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    command : str
        The base command to execute (e.g., "ls", "echo").
    args : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The combined stdout and stderr output of the executed command.

    Raises
    ------
    ValueError
        If the command is empty, not a string, or the execution fails.
    """
    if not isinstance(command, str) or not command.strip():
        raise ValueError("Command must be a non-empty string")

    if not isinstance(args, list):
        raise ValueError("Arguments must be provided as a list")

    # Build the full command list
    cmd = [command] + args

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,  # We handle errors manually
        )
    except OSError as e:
        raise ValueError(f"Execution failed: {e}") from e

    if result.returncode != 0:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command '{command}' exited with code {result.returncode}: "
            f"{result.stderr.strip()}"
        )

    return result.stdout