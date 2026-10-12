import subprocess
import shlex
from shutil import which

def execute_command(cmd: str, arguments: list) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    cmd : str
        The command to execute (e.g., "ls", "grep").
    arguments : list
        A list of string arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be found or execution fails.
    """
    # Ensure the command exists on the system
    if not isinstance(cmd, str) or not cmd:
        raise ValueError("Command must be a non-empty string")

    # Use which() to locate the executable and avoid shell injection
    executable = which(cmd)
    if not executable:
        raise ValueError(f"Command '{cmd}' not found in PATH")

    # Build the full argument list
    if not isinstance(arguments, list):
        raise ValueError("Arguments must be a list")
    # Convert each argument to string safely
    safe_args = [str(arg) for arg in arguments]

    # Run the command without invoking a shell
    try:
        result = subprocess.run(
            [executable] + safe_args,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise ValueError(
            f"Command '{cmd}' failed with exit code {e.returncode}"
        ) from e
    except Exception as e:
        raise ValueError(f"Failed to execute command '{cmd}': {e}") from e

    return result.stdout