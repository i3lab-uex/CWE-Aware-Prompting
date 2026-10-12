import subprocess
import shlex
from typing import List


def execute_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    cmd : str
        The base command to run (e.g., 'ls', 'python').
    arguments : list
        A list of argument strings to pass to the command.

    Returns
    -------
    str
        The decoded standard output of the command.

    Raises
    ------
    ValueError
        If the command cannot be executed, is invalid, or returns a non-zero exit status.
    """
    # Build the full argument list
    full_cmd = [cmd] + arguments

    try:
        # Run the command without invoking a shell to avoid shell injection
        result = subprocess.run(
            full_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,          # automatically decode bytes to str
            check=False         # we handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd}") from exc
    except OSError as exc:
        raise ValueError(f"Failed to execute command '{cmd}': {exc}") from exc

    # If the command exited with a non-zero status, treat it as an error
    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd}' failed with exit code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout