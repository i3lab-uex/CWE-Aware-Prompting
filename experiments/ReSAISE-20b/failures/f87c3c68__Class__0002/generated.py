import subprocess
import shlex
import shutil
from typing import List

def run_shell_command(shell_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the supplied arguments and return its output.

    Parameters
    ----------
    shell_command : str
        The base command to execute (e.g., "ls", "grep").
    parameters : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output of the executed command.

    Raises
    ------
    ValueError
        If the command cannot be found or if execution fails.
    """
    # Ensure the command exists on the system
    cmd_path = shutil.which(shell_command)
    if not cmd_path:
        raise ValueError(f"Command '{shell_command}' not found in PATH.")

    # Build the argument list safely; do not use shell=True to avoid injection
    cmd = [cmd_path] + parameters

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,          # Raises CalledProcessError on non-zero exit
        )
    except subprocess.CalledProcessError as exc:
        # Provide a clear error message with stdout/stderr
        raise ValueError(
            f"Command '{shell_command}' failed with exit code {exc.returncode}.\n"
            f"Stdout: {exc.stdout}\nStderr: {exc.stderr}"
        ) from exc
    except Exception as exc:
        # Catch any other unexpected errors (e.g., permission denied)
        raise ValueError(f"Failed to execute command '{shell_command}': {exc}") from exc

    return result.stdout