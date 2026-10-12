import subprocess
import shlex
from typing import List


def run_shell_cmd(cmd_name: str, cmd_args: List[str]) -> str:
    """
    Execute a shell command and return its output.

    Parameters
    ----------
    cmd_name : str
        The main executable to run.
    cmd_args : list[str]
        Arguments to pass to the command.

    Returns
    -------
    str
        The combined stdout and stderr of the executed command.

    Raises
    ------
    ValueError
        If the command cannot be found, or if it exits with a non‑zero status.
    """
    # Build the command list.  Using a list avoids shell injection problems.
    cmd = [cmd_name] + cmd_args

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False  # We'll handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd_name}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command: {shlex.join(cmd)}") from exc

    # Combine stdout and stderr for easier debugging
    output = result.stdout + ("\n" if result.stdout and result.stderr else "") + result.stderr

    if result.returncode != 0:
        raise ValueError(
            f"Command '{shlex.join(cmd)}' exited with status {result.returncode}\nOutput:\n{output}"
        )

    return output.strip()