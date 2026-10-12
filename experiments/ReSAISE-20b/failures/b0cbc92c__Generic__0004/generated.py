import subprocess
import shlex
from typing import List

def run_command(cmd: str, cmd_arguments: List[str]) -> str:
    """
    Execute a shell command with the supplied arguments and return its output.

    Parameters
    ----------
    cmd : str
        The main command to run (e.g., "ls", "git").
    cmd_arguments : list
        A list of string arguments to pass to the command.

    Returns
    -------
    str
        The combined stdout and stderr output of the executed command.

    Raises
    ------
    ValueError
        If the command is empty, arguments are not a list of strings,
        or if the subprocess fails to execute successfully.
    """
    # Basic validation
    if not isinstance(cmd, str) or not cmd.strip():
        raise ValueError("Command must be a non-empty string")

    if not isinstance(cmd_arguments, list) or any(
        not isinstance(arg, str) for arg in cmd_arguments
    ):
        raise ValueError("cmd_arguments must be a list of strings")

    # Build the full command list
    full_cmd = [cmd] + cmd_arguments

    try:
        # Execute the command safely; capture output and errors
        result = subprocess.run(
            full_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,  # We handle errors manually
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {cmd}") from e
    except OSError as e:
        raise ValueError(f"Failed to execute command: {e}") from e

    # If the command exited with a non-zero status, raise an error
    if result.returncode != 0:
        error_msg = (
            f"Command '{cmd}' failed with return code {result.returncode}.\n"
            f"stderr: {result.stderr.strip()}"
        )
        raise ValueError(error_msg)

    # Return the captured stdout (or both stdout and stderr if desired)
    return result.stdout.strip()