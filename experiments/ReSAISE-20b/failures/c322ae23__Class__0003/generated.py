import subprocess
from typing import List


def run_command_with_args(base_command: str, parameters: List[str]) -> str:
    """
    Execute a command with the given arguments and return its output.

    Parameters
    ----------
    base_command : str
        The primary command to run (e.g., "ls", "grep").
    parameters : list[str]
        A list of arguments for the command.

    Returns
    -------
    str
        The standard output produced by the command, stripped of trailing newlines.

    Raises
    ------
    ValueError
        If the command is empty, if any argument is not a string,
        or if the process exits with a non‑zero return code.
    """
    # Basic validation
    if not isinstance(base_command, str) or not base_command.strip():
        raise ValueError("base_command must be a non‑empty string")

    if not isinstance(parameters, list):
        raise ValueError("parameters must be a list")

    for arg in parameters:
        if not isinstance(arg, str):
            raise ValueError("all elements of parameters must be strings")

    # Build the command list; no shell expansion is performed.
    cmd = [base_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False  # We handle non‑zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {base_command}") from exc
    except OSError as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        err_msg = result.stderr.strip() or "Unknown error"
        raise ValueError(f"Command '{base_command}' failed with exit code {result.returncode}: {err_msg}")

    return result.stdout.strip()