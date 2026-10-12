import shlex
import subprocess
from typing import List


def run_shell_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    cmd : str
        The base command to execute (e.g., "ls", "git").
    arguments : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The stdout output from the executed command.

    Raises
    ------
    ValueError
        If the command cannot be found, is not executable,
        or returns a non‑zero exit status.
    """
    if not isinstance(cmd, str) or not cmd.strip():
        raise ValueError("Command must be a non‑empty string")

    if not isinstance(arguments, list):
        raise ValueError("Arguments must be a list")

    # Build the command safely as a list of arguments.
    # Each element is already provided by the caller; we do not join them into a string
    # to avoid shell injection.  However, if the caller provides a single string
    # containing multiple tokens, we use shlex.split to tokenize it.
    cmd_parts = [cmd]
    for arg in arguments:
        if isinstance(arg, str):
            # If the argument itself contains spaces or shell meta‑characters,
            # split it safely and extend the list.
            cmd_parts.extend(shlex.split(arg))
        else:
            # Non‑string arguments are converted to string representation.
            cmd_parts.append(str(arg))

    try:
        result = subprocess.run(
            cmd_parts,
            capture_output=True,
            text=True,
            check=False,  # We handle non‑zero exit manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd}") from exc
    except PermissionError as exc:
        raise ValueError(f"Permission denied executing: {cmd}") from exc
    except OSError as exc:
        raise ValueError(f"Failed to execute command '{cmd}': {exc}") from exc

    if result.returncode != 0:
        error_msg = (
            f"Command '{cmd}' exited with code {result.returncode}.\n"
            f"stderr: {result.stderr.strip()}"
        )
        raise ValueError(error_msg)

    return result.stdout