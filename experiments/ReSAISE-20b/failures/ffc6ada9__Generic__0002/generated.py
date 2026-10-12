import subprocess
from typing import List

def execute_command(base_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the given parameters and return its output.

    Parameters
    ----------
    base_command : str
        The primary command to run (e.g., "ls", "echo").
    parameters : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the base_command is empty, parameters contain non-string items,
        or the command fails to execute.
    """
    if not isinstance(base_command, str) or not base_command.strip():
        raise ValueError("base_command must be a non-empty string")

    if not isinstance(parameters, list):
        raise ValueError("parameters must be a list of strings")

    for i, arg in enumerate(parameters):
        if not isinstance(arg, str):
            raise ValueError(f"parameter at index {i} is not a string")

    # Build the command as a list to avoid shell injection
    cmd = [base_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False  # We'll handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {base_command}") from exc
    except OSError as exc:
        raise ValueError(f"Execution failed: {exc}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{base_command}' failed with return code {result.returncode}\n"
            f"stderr: {result.stderr.strip()}"
        )

    return result.stdout