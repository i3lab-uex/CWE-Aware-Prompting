import subprocess
from typing import List

def execute_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    cmd : str
        The executable command (e.g., 'ls', 'python').
    arguments : List[str]
        A list of string arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed, is not found, or returns a non‑zero exit status.
    """
    if not isinstance(cmd, str):
        raise ValueError("cmd must be a string")
    if not isinstance(arguments, list) or not all(isinstance(a, str) for a in arguments):
        raise ValueError("arguments must be a list of strings")

    # Build the full command sequence
    cmd_list = [cmd] + arguments

    try:
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            check=False,          # we handle errors ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command '{cmd}': {exc}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd}' exited with status {result.returncode}.\n"
            f"Stderr: {result.stderr.strip()}"
        )

    return result.stdout