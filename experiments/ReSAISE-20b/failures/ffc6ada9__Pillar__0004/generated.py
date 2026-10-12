import subprocess
from typing import List

def execute_command(base_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    base_command : str
        The main command to run (e.g., "ls", "git").
    parameters : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If `base_command` is empty, `parameters` contains non‑string items,
        or the command exits with a non‑zero return code.
    """
    # Basic input validation
    if not isinstance(base_command, str) or not base_command.strip():
        raise ValueError("base_command must be a non‑empty string")

    if not isinstance(parameters, list):
        raise ValueError("parameters must be a list of strings")

    for arg in parameters:
        if not isinstance(arg, str):
            raise ValueError("All items in parameters must be strings")

    # Build the command list for subprocess
    cmd = [base_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,          # We'll handle non‑zero exit codes ourselves
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {base_command}") from e
    except Exception as e:
        raise ValueError(f"Failed to execute command: {e}") from e

    if result.returncode != 0:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command '{base_command}' exited with code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout