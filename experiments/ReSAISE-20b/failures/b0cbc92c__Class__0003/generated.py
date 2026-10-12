import subprocess
import shlex
import shutil
from typing import List

def run_command(cmd: str, cmd_arguments: List[str]) -> str:
    """
    Execute a shell command safely and return its output.

    Parameters
    ----------
    cmd : str
        The main executable to run.
    cmd_arguments : list[str]
        List of arguments for the command.

    Returns
    -------
    str
        The decoded stdout from the executed process.

    Raises
    ------
    ValueError
        If the command is empty, not found in PATH, or fails to execute.
    """
    if not cmd:
        raise ValueError("Command must be a non-empty string")

    # Resolve the command to an absolute path to avoid shell interpretation
    cmd_path = shutil.which(cmd)
    if not cmd_path:
        raise ValueError(f"Command '{cmd}' not found in PATH")

    # Build the argument list. Each element is passed literally to the process.
    command = [cmd_path] + cmd_arguments

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True  # Raises CalledProcessError on non‑zero exit status
        )
    except subprocess.CalledProcessError as exc:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command '{cmd}' failed with exit code {exc.returncode}:\n{exc.stderr}"
        ) from exc
    except OSError as exc:
        # Handles cases where the executable cannot be started
        raise ValueError(f"Failed to execute command '{cmd}': {exc}") from exc

    return result.stdout