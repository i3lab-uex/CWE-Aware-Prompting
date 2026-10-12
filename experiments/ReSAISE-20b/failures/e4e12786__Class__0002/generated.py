import subprocess
import shlex
from shutil import which
from typing import List


def execute_shell_command(command: str, args: List[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    command : str
        The base command to execute (e.g., "ls", "echo").
    args : list[str]
        A list of arguments for the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the base command is not found, if execution fails, or if
        any argument contains disallowed characters.
    """
    # Ensure the command exists on the system path
    if which(command) is None:
        raise ValueError(f"Command '{command}' not found in PATH")

    # Reject potentially dangerous characters that could alter command semantics
    disallowed_chars = {";", "&", "|", "$", "`", ">", "<", "\\"}
    for arg in args:
        if any(ch in disallowed_chars for ch in arg):
            raise ValueError(f"Argument '{arg}' contains disallowed characters")

    # Build the command list safely (no shell=True)
    cmd = [command] + args

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,          # Raise CalledProcessError on non-zero exit
        )
    except subprocess.CalledProcessError as exc:
        # Include stderr in the error message for easier debugging
        raise ValueError(
            f"Command '{command}' failed with exit code {exc.returncode}: "
            f"{exc.stderr.strip()}"
        ) from exc
    except OSError as exc:
        # Handle cases where the command cannot be executed (e.g., permission denied)
        raise ValueError(f"Execution failed for '{command}': {exc}") from exc

    return result.stdout.strip()