import subprocess
import shlex
import shutil
from typing import List


def execute_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the given list of arguments and return its output.

    Parameters
    ----------
    cmd : str
        The command to execute (e.g., "ls", "python").
    arguments : list[str]
        A list of string arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be found, if execution fails, or if a non‑zero exit code
        is returned.
    """
    # Ensure the command exists in PATH to avoid executing arbitrary binaries
    if shutil.which(cmd) is None:
        raise ValueError(f"Command '{cmd}' not found in PATH")

    # Build the command list safely; avoid shell=True to prevent injection
    cmd_list = [cmd] + arguments

    try:
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            check=False,          # we handle non‑zero exit codes manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Failed to start command '{cmd}': {exc}") from exc
    except OSError as exc:
        raise ValueError(f"OS error while executing '{cmd}': {exc}") from exc

    if result.returncode != 0:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command '{cmd}' exited with non‑zero status {result.returncode}:\n"
            f"stderr: {result.stderr.strip()}"
        )

    return result.stdout