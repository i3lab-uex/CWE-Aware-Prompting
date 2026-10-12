import subprocess
import shlex
from typing import List

def run_shell_command(shell_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    shell_command : str
        The base command to execute (e.g., "ls", "git").
    parameters : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed, is not found, or returns a non‑zero exit status.
    """
    # Build the command list safely
    try:
        cmd = [shell_command] + parameters
        # Ensure the command is a list of strings (already safe)
    except Exception as exc:
        raise ValueError(f"Failed to build command: {exc}") from exc

    try:
        # Run the process without using a shell for security
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False  # We will handle non-zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {shell_command}") from exc
    except OSError as exc:
        raise ValueError(f"Execution failed: {exc}") from exc

    if result.returncode != 0:
        # Include stderr in the error message for debugging
        err_msg = result.stderr.strip() or "Unknown error"
        raise ValueError(f"Command '{shell_command}' failed with exit code {result.returncode}: {err_msg}")

    return result.stdout.strip()