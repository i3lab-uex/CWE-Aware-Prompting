import subprocess
import shlex
from shutil import which
from typing import List


def run_shell_command(shell_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    shell_command : str
        The base command to run (e.g., 'ls', 'grep').
    parameters : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed or is invalid.
    """
    # Ensure the base command exists in PATH
    if not which(shell_command):
        raise ValueError(f"Command '{shell_command}' not found in PATH.")

    # Build the full command list; each element is a separate argument
    cmd = [shell_command] + parameters

    try:
        # Run the command without invoking a shell to avoid injection
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,          # returns strings instead of bytes
            check=True          # raise CalledProcessError on non‑zero exit
        )
    except subprocess.CalledProcessError as exc:
        # Capture stderr for debugging but raise a ValueError to match spec
        error_msg = (
            f"Command '{shlex.join(cmd)}' failed with exit code {exc.returncode}.\n"
            f"Stderr: {exc.stderr.strip()}"
        )
        raise ValueError(error_msg) from exc
    except OSError as exc:
        # e.g., permission denied, file not found, etc.
        raise ValueError(f"Failed to execute command '{shell_command}': {exc}") from exc

    return result.stdout.strip()