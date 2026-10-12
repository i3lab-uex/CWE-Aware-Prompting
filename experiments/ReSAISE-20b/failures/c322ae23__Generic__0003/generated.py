import subprocess
import shlex
import shutil
from typing import List


def run_command_with_args(base_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the supplied arguments and return its output.

    Parameters
    ----------
    base_command : str
        The primary command to run (e.g., "ls", "git").
    parameters : list[str]
        A list of arguments for the command.

    Returns
    -------
    str
        The standard output produced by the command (decoded as text).

    Raises
    ------
    ValueError
        If the command is not found, if parameters are invalid,
        or if the command exits with a non‑zero status.
    """
    # Basic validation
    if not isinstance(base_command, str) or not base_command:
        raise ValueError("base_command must be a non‑empty string")

    if not isinstance(parameters, list):
        raise ValueError("parameters must be a list of strings")
    for arg in parameters:
        if not isinstance(arg, str):
            raise ValueError("each parameter must be a string")

    # Ensure the command exists in PATH
    if shutil.which(base_command) is None:
        raise ValueError(f"Command '{base_command}' not found in PATH")

    # Construct the full command list
    cmd = [base_command] + parameters

    try:
        # Run the command, capture stdout and stderr
        result = subprocess.run(
            cmd,
            check=True,
            text=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as exc:
        # Provide useful information in the error
        raise ValueError(
            f"Command '{base_command}' failed with exit code {exc.returncode}\n"
            f"stderr: {exc.stderr.strip()}"
        ) from exc
    except OSError as exc:
        raise ValueError(f"Execution failed: {exc}") from exc

    return result.stdout.strip()