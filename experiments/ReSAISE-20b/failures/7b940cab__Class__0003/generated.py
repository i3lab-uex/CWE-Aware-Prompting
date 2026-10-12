import subprocess
from typing import List


def execute_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    cmd : str
        The command to run (e.g., "ls", "echo").
    arguments : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The stdout produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed, is not found, or returns a non‑zero exit status.
    """
    # Build the argument list.  Do NOT use shell=True to avoid command injection
    command = [cmd] + arguments

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,   # we will handle non‑zero exit ourselves
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {cmd}") from e
    except OSError as e:
        raise ValueError(f"Failed to execute command '{cmd}': {e}") from e

    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd}' failed with exit code {result.returncode}.\n"
            f"stderr: {result.stderr.strip()}"
        )

    return result.stdout