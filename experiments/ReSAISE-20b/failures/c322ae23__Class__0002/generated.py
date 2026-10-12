import subprocess
import shlex
from shutil import which
from typing import List


def run_command_with_args(base_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with user‑supplied arguments and return its output.

    Parameters
    ----------
    base_command : str
        The primary command to run (e.g. "ls", "git").
    parameters : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the executed command.

    Raises
    ------
    ValueError
        If the base command is not found, if any argument is not a string,
        or if the command exits with a non‑zero status.
    """
    # Validate that the base command exists in the PATH
    if not which(base_command):
        raise ValueError(f"Command '{base_command}' not found in PATH")

    # Ensure all parameters are strings
    if any(not isinstance(p, str) for p in parameters):
        raise ValueError("All parameters must be strings")

    # Build the command list; passing a list avoids shell interpretation
    cmd = [base_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,          # Raises CalledProcessError on non‑zero exit
        )
    except subprocess.CalledProcessError as exc:
        # Combine stdout and stderr for richer debugging information
        error_msg = (
            f"Command '{base_command}' failed with exit code {exc.returncode}\n"
            f"stdout: {exc.stdout}\nstderr: {exc.stderr}"
        )
        raise ValueError(error_msg) from exc

    return result.stdout