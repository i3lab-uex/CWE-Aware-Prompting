import subprocess
import shlex
import shutil
from typing import List

def execute_command(base_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command safely and return its output.

    Parameters
    ----------
    base_command : str
        The main executable to run (e.g., "ls", "python").
    parameters : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded stdout from the executed command.

    Raises
    ------
    ValueError
        If the base_command is empty, not found in PATH,
        or if the subprocess fails to execute.
    """
    # Basic validation
    if not isinstance(base_command, str) or not base_command.strip():
        raise ValueError("base_command must be a non-empty string")

    if not isinstance(parameters, list):
        raise ValueError("parameters must be a list of strings")

    # Ensure all parameters are strings
    for idx, param in enumerate(parameters):
        if not isinstance(param, str):
            raise ValueError(f"parameter at index {idx} is not a string")

    # Verify that the command exists in PATH
    if shutil.which(base_command) is None:
        raise ValueError(f"Command '{base_command}' not found in PATH")

    # Build the command list safely (no shell=True)
    cmd = [base_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False  # We'll handle errors manually
        )
    except OSError as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        # Include stderr in the error message for better debugging
        raise ValueError(
            f"Command '{base_command}' exited with code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout