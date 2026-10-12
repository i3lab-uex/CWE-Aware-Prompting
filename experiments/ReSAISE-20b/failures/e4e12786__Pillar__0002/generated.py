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
        The base command to execute.
    args : list[str]
        A list of arguments for the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command is not found, cannot be executed,
        or if the execution fails.
    """
    # Ensure command is a string
    if not isinstance(command, str):
        raise ValueError("Command must be a string")

    # Ensure args is a list of strings
    if not isinstance(args, list) or not all(isinstance(a, str) for a in args):
        raise ValueError("Arguments must be a list of strings")

    # Resolve the full path to the command to avoid shell injection
    cmd_path = shutil.which(command)
    if not cmd_path:
        raise ValueError(f"Command '{command}' not found in PATH")

    # Build the full argument list
    full_cmd = [cmd_path] + args

    try:
        # Execute without invoking the shell to avoid injection risks
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            check=True,          # Raise CalledProcessError on non-zero exit
        )
    except subprocess.CalledProcessError as exc:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command '{command}' failed with exit code {exc.returncode}: "
            f"{exc.stderr.strip()}"
        ) from exc
    except Exception as exc:
        # Generic error handling for unexpected exceptions
        raise ValueError(f"Failed to execute command '{command}': {exc}") from exc

    return result.stdout