import subprocess
import shlex
import shutil
from typing import List


def call_system_command(sys_command: str, params: List[str]) -> str:
    """
    Execute a system command with the provided arguments.

    Parameters
    ----------
    sys_command : str
        The primary executable to run.
    params : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output from the executed command.

    Raises
    ------
    ValueError
        If the executable cannot be found or the command exits with a non‑zero status.
    """
    # Resolve full path to prevent accidental shell execution
    executable = shutil.which(sys_command)
    if not executable:
        raise ValueError(f"Command '{sys_command}' not found in PATH")

    # Construct the command list; avoid shell=True to prevent injection
    cmd = [executable] + params

    try:
        # Run the command, capture stdout and stderr
        result = subprocess.run(
            cmd,
            check=True,
            text=True,
            capture_output=True
        )
    except subprocess.CalledProcessError as exc:
        # Include stderr in the exception message for debugging
        raise ValueError(
            f"Command '{sys_command}' failed with exit code {exc.returncode}: "
            f"{exc.stderr.strip()}"
        ) from exc
    except OSError as exc:
        # Handle cases where the executable cannot be started
        raise ValueError(f"Failed to start command '{sys_command}': {exc}") from exc

    return result.stdout.strip()