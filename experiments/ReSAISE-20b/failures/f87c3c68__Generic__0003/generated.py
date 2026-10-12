import subprocess
import shlex
from typing import List


def run_shell_command(shell_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    shell_command : str
        The base command to execute (e.g., "ls", "grep").
    parameters : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed or returns a non‑zero exit status.
    """
    # Build the full command list safely
    cmd_parts = [shell_command] + parameters

    try:
        # Run the command without invoking a shell for security
        result = subprocess.run(
            cmd_parts,
            capture_output=True,
            text=True,
            check=False,          # We'll handle errors manually
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {shell_command}") from e
    except OSError as e:
        raise ValueError(f"Failed to execute command: {shell_command}") from e

    if result.returncode != 0:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command '{shell_command}' failed with exit code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout