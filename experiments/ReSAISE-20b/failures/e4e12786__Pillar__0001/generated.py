import subprocess
import shlex
from shutil import which
from typing import List

def execute_shell_command(command: str, args: List[str]) -> str:
    """
    Execute a shell command with the supplied arguments and return its stdout output.

    Parameters
    ----------
    command : str
        The base executable to run (e.g., "ls", "python").
    args : list
        A list of arguments for the command. Each argument should be a string.

    Returns
    -------
    str
        The decoded stdout output of the command.

    Raises
    ------
    ValueError
        If the command is not found, if it exits with a non‑zero status,
        or if any other execution error occurs.
    """
    # Ensure the command exists in PATH
    if not which(command):
        raise ValueError(f"Command '{command}' not found in PATH")

    # Build the full command list
    cmd = [command] + args

    try:
        result = subprocess.run(
            cmd,
            check=True,                     # Raises CalledProcessError on non‑zero exit
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,        # Merge stderr into stdout for simplicity
            text=True,                      # Decode bytes to str using locale encoding
        )
    except subprocess.CalledProcessError as exc:
        raise ValueError(
            f"Command '{command}' failed with exit code {exc.returncode}: "
            f"{exc.output.strip()}"
        ) from exc
    except OSError as exc:
        # Covers cases like permission denied, not executable, etc.
        raise ValueError(f"Execution failed for '{command}': {exc}") from exc

    return result.stdout.strip()