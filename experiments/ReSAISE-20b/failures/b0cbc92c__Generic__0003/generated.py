import subprocess
from typing import List


def run_command(cmd: str, cmd_arguments: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    cmd : str
        The main command to execute.
    cmd_arguments : list[str]
        List of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output of the executed command.

    Raises
    ------
    ValueError
        If the command fails to execute or returns a non‑zero exit status.
    """
    if not isinstance(cmd, str) or not cmd:
        raise ValueError("`cmd` must be a non‑empty string")

    if not isinstance(cmd_arguments, list):
        raise ValueError("`cmd_arguments` must be a list")

    # Build the full command as a list for subprocess
    full_cmd = [cmd] + cmd_arguments

    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,          # decode bytes to str automatically
            check=False         # we handle non‑zero ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd}") from exc
    except OSError as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        err_msg = result.stderr.strip() or f"Command exited with status {result.returncode}"
        raise ValueError(f"Command failed: {err_msg}")

    return result.stdout.strip()