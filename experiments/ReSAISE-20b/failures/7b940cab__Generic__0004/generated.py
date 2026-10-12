import subprocess
import shlex
from typing import List


def execute_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    cmd : str
        The command to execute (e.g., "ls", "python").
    arguments : list[str]
        List of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed, is not found, or returns a non‑zero exit status.
    """
    if not isinstance(cmd, str) or not cmd.strip():
        raise ValueError("`cmd` must be a non‑empty string")

    if not isinstance(arguments, list):
        raise ValueError("`arguments` must be a list")

    # Build the argument list safely.  Use shlex.split to handle quoted arguments
    # if `cmd` contains spaces (e.g., "python -m").
    cmd_parts = shlex.split(cmd) if ' ' in cmd else [cmd]
    full_command = cmd_parts + arguments

    try:
        result = subprocess.run(
            full_command,
            capture_output=True,
            text=True,
            check=False  # We'll handle non‑zero return codes ourselves
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {cmd}") from e
    except OSError as e:
        raise ValueError(f"Failed to execute command '{cmd}': {e}") from e

    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd}' exited with code {result.returncode}:\n{result.stderr}"
        )

    return result.stdout