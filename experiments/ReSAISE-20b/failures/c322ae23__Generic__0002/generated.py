import subprocess
from typing import List

def run_command_with_args(base_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    base_command : str
        The primary command to run (e.g., "ls", "git").
    parameters : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command, stripped of trailing newlines.

    Raises
    ------
    ValueError
        If the command fails to execute or returns a non‑zero exit status.
    """
    if not isinstance(base_command, str) or not base_command:
        raise ValueError("base_command must be a non-empty string")

    if not isinstance(parameters, list):
        raise ValueError("parameters must be a list of strings")

    # Ensure all parameters are strings
    for p in parameters:
        if not isinstance(p, str):
            raise ValueError("All elements in parameters must be strings")

    # Build the command list
    cmd = [base_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,          # Raises CalledProcessError on non-zero exit
        )
    except (subprocess.CalledProcessError, OSError) as exc:
        raise ValueError(f"Command execution failed: {exc}") from exc

    return result.stdout.strip()