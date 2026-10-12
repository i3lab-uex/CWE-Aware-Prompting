import subprocess
import shlex
from typing import List

def run_shell_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the provided list of arguments and return its output.

    Parameters
    ----------
    cmd : str
        The base command to run (e.g., 'ls', 'git').
    arguments : list[str]
        A list of command‑line arguments to pass to the command.

    Returns
    -------
    str
        The decoded stdout of the executed process.

    Raises
    ------
    ValueError
        If ``cmd`` is empty, or if the command fails to execute (non‑zero exit status
        or any exception raised by :class:`subprocess`).
    """
    if not isinstance(cmd, str) or not cmd.strip():
        raise ValueError("`cmd` must be a non‑empty string")

    if not isinstance(arguments, list):
        raise ValueError("`arguments` must be a list of strings")

    # Build the command list safely
    full_cmd = [cmd] + arguments

    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            check=False,          # We'll handle non‑zero exit codes ourselves
        )
    except (OSError, ValueError) as exc:
        # OSError: e.g., command not found
        raise ValueError(f"Failed to execute command '{cmd}': {exc}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd}' failed with exit code {result.returncode}.\n"
            f"Stderr: {result.stderr.strip()}"
        )

    return result.stdout