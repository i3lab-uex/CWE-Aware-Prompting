import subprocess
from typing import List


def run_shell_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    cmd : str
        The base command to run (e.g., 'ls', 'python').
    arguments : list
        A list of string arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command is invalid, cannot be found, or exits with a non‑zero status.
    """
    if not cmd:
        raise ValueError("Command must be a non-empty string")

    # Build the command list: [cmd, arg1, arg2, ...]
    full_cmd = [cmd] + list(arguments)

    try:
        result = subprocess.run(
            full_cmd,
            check=True,          # raise CalledProcessError on non‑zero exit
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,           # return string instead of bytes
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd}") from exc
    except subprocess.CalledProcessError as exc:
        raise ValueError(
            f"Command '{cmd}' failed with exit code {exc.returncode}:\n{exc.output}"
        ) from exc

    return result.stdout