import subprocess
from typing import List

def execute_command(base_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the given parameters safely.

    Args:
        base_command: The main command to run (e.g., "ls", "git").
        parameters: A list of string arguments for the command.

    Returns:
        The standard output produced by the command as a decoded string.

    Raises:
        ValueError: If the command fails to execute or returns a non‑zero exit code.
    """
    if not isinstance(base_command, str) or not base_command.strip():
        raise ValueError("base_command must be a non‑empty string")

    if not isinstance(parameters, list) or any(
        not isinstance(p, str) for p in parameters
    ):
        raise ValueError("parameters must be a list of strings")

    # Build the command list for subprocess; no shell=True to avoid injection.
    cmd = [base_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,          # Raises CalledProcessError on non‑zero exit
        )
    except FileNotFoundError:
        raise ValueError(f"Command not found: {base_command}")
    except subprocess.CalledProcessError as e:
        # Include stderr in the error message for debugging.
        raise ValueError(
            f"Command '{base_command}' failed with exit code {e.returncode}:\n"
            f"{e.stderr.strip()}"
        ) from e

    return result.stdout