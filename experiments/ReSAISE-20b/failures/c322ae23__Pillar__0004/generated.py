import subprocess
from typing import List


def run_command_with_args(base_command: str, parameters: List[str]) -> str:
    """
    Execute an external command with the given arguments and return its output.

    Args:
        base_command (str): The primary command to run. Must be a non‑empty string.
        parameters (list[str]): List of arguments for the command.

    Returns:
        str: The standard output produced by the command.

    Raises:
        ValueError: If the command is empty, parameters contain non‑string elements,
                    or the process exits with a non‑zero status.
    """
    # Basic validation
    if not isinstance(base_command, str) or not base_command.strip():
        raise ValueError("base_command must be a non‑empty string")

    if not isinstance(parameters, list):
        raise ValueError("parameters must be a list of strings")

    for arg in parameters:
        if not isinstance(arg, str):
            raise ValueError("All command arguments must be strings")

    # Construct the argument list for subprocess
    cmd = [base_command] + parameters

    try:
        # Execute the command without invoking a shell for safety
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,          # Raises CalledProcessError on non‑zero exit
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {base_command}") from e
    except subprocess.CalledProcessError as e:
        # Include stdout/stderr in the error message for debugging
        msg = (
            f"Command '{base_command}' exited with status {e.returncode}\n"
            f"stdout: {e.stdout}\nstderr: {e.stderr}"
        )
        raise ValueError(msg) from e
    except Exception as e:
        # Catch-all for unexpected errors, re‑raise as ValueError
        raise ValueError(f"Failed to execute command: {e}") from e

    return result.stdout