import subprocess
from typing import List


def run_shell_cmd(cmd: str, params: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its stdout output.

    Parameters
    ----------
    cmd : str
        The command to execute (e.g., 'ls', 'python').
    params : list[str]
        List of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output from the executed command.

    Raises
    ------
    ValueError
        If the command cannot be executed, if it exits with a non‑zero status,
        or if an error occurs during the subprocess call.
    """
    # Build a list of arguments: first element is the command, followed by params
    if not isinstance(cmd, str):
        raise ValueError("Command must be a string")
    if not isinstance(params, list) or any(not isinstance(p, str) for p in params):
        raise ValueError("Params must be a list of strings")

    # Use subprocess.run with shell=False to avoid command injection
    try:
        result = subprocess.run(
            [cmd] + params,
            capture_output=True,
            text=True,
            check=False  # we will handle non‑zero exit codes ourselves
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {cmd}") from e
    except Exception as e:
        raise ValueError(f"Failed to execute command '{cmd}': {e}") from e

    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd}' exited with status {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout