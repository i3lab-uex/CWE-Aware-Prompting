import subprocess
import shlex
from typing import List

def run_command(cmd: str, cmd_arguments: List[str]) -> str:
    """
    Execute a shell command safely and return its output.

    Parameters
    ----------
    cmd : str
        The main executable to run.
    cmd_arguments : list[str]
        Arguments to pass to the command.

    Returns
    -------
    str
        The stdout produced by the command.

    Raises
    ------
    ValueError
        If the command is invalid, cannot be executed,
        or if the subprocess returns a non‑zero exit status.
    """
    # Basic validation
    if not isinstance(cmd, str) or not cmd.strip():
        raise ValueError("Command must be a non‑empty string.")

    if not isinstance(cmd_arguments, list):
        raise ValueError("cmd_arguments must be a list.")

    for arg in cmd_arguments:
        if not isinstance(arg, str):
            raise ValueError("All command arguments must be strings.")

    # Build the argument list for subprocess.run
    # Use shlex.quote only when we need a single string representation,
    # but here we pass a list so no shell interpolation occurs.
    full_cmd = [cmd] + cmd_arguments

    try:
        result = subprocess.run(
            full_cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,  # ensures output is str
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {cmd}") from e
    except subprocess.CalledProcessError as e:
        # The command executed but returned a non‑zero exit status
        raise ValueError(
            f"Command '{cmd}' failed with exit code {e.returncode}. "
            f"Output:\n{e.output}"
        ) from e
    except Exception as e:
        # Catch-all for other subprocess related errors
        raise ValueError(f"Failed to run command '{cmd}': {e}") from e

    return result.stdout