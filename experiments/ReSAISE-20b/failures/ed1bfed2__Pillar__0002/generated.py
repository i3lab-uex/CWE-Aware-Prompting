import subprocess
import shlex
import shutil
from typing import List


def run_shell_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    cmd : str
        The primary command to run (e.g., 'ls', 'git').
    arguments : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The stdout produced by the command.

    Raises
    ------
    ValueError
        If the command is not found, fails to execute, or returns a non‑zero exit status.
    """
    # Ensure the base command exists on the system
    if shutil.which(cmd) is None:
        raise ValueError(f"Command not found: {cmd}")

    # Build the full command list
    cmd_list = [cmd] + arguments

    try:
        # Execute the command without invoking a shell
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            check=False  # we handle non‑zero exit codes manually
        )
    except Exception as exc:          # pragma: no cover
        raise ValueError(f"Failed to execute command '{cmd}': {exc}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd}' exited with status {result.returncode}.\n"
            f"stderr: {result.stderr.strip()}"
        )

    return result.stdout