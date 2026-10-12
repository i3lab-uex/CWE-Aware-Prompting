import subprocess
from typing import List


def run_shell_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    cmd : str
        The base command to run (e.g., "ls", "echo").
    arguments : list
        A list of argument strings to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed or returns a non‑zero exit status.
    """
    if not isinstance(cmd, str):
        raise ValueError("cmd must be a string")
    if not isinstance(arguments, list) or any(not isinstance(a, str) for a in arguments):
        raise ValueError("arguments must be a list of strings")

    # Build the command as a list to avoid shell interpolation
    cmd_list = [cmd] + arguments

    try:
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            check=False  # We handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd}") from exc
    except OSError as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        err_msg = (
            f"Command '{cmd}' failed with exit code {result.returncode}\n"
            f"stderr: {result.stderr.strip()}"
        )
        raise ValueError(err_msg)

    return result.stdout