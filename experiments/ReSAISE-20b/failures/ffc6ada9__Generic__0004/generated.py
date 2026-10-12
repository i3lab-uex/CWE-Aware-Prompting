import subprocess
from typing import List


def execute_command(base_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    base_command : str
        The primary command to run (e.g., "ls", "git").
    parameters : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the base_command is empty, if any parameter is not a string,
        or if the command execution fails (non‑zero exit status).
    """
    # Basic validation
    if not isinstance(base_command, str) or not base_command.strip():
        raise ValueError("base_command must be a non‑empty string")

    if not isinstance(parameters, list):
        raise ValueError("parameters must be a list of strings")

    for idx, param in enumerate(parameters):
        if not isinstance(param, str):
            raise ValueError(f"parameter at index {idx} is not a string")

    # Build the command list for subprocess
    cmd = [base_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,  # We'll handle errors ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {base_command}") from exc
    except OSError as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command '{base_command}' failed with exit code {result.returncode}:\n{result.stderr.strip()}"
        )

    return result.stdout