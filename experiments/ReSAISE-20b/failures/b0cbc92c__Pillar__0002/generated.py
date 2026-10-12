import subprocess
from typing import List

def run_command(cmd: str, cmd_arguments: List[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    cmd : str
        The base command to run (e.g., "ls", "git").
    cmd_arguments : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The stdout produced by the command.

    Raises
    ------
    ValueError
        If the command fails to execute or returns a non‑zero exit status.
    """
    if not isinstance(cmd, str) or not cmd.strip():
        raise ValueError("Command must be a non‑empty string")

    if not isinstance(cmd_arguments, list):
        raise ValueError("cmd_arguments must be a list")

    # Build the argument list safely; do not use shell=True
    args = [cmd] + cmd_arguments

    try:
        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False  # We handle non‑zero exit codes manually
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {cmd}") from e
    except OSError as e:
        raise ValueError(f"Failed to execute command: {e}") from e

    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd}' exited with status {result.returncode}: "
            f"{result.stderr.strip()}"
        )

    return result.stdout