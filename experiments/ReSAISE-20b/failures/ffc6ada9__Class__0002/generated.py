import subprocess
from typing import List

def execute_command(base_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command safely and return its output.

    Args:
        base_command: The main executable to run (e.g., "ls", "echo").
        parameters: A list of arguments to pass to the command.

    Returns:
        The decoded stdout from the executed command.

    Raises:
        ValueError: If the command is empty, not a string,
                    or if execution fails (non‑zero return code).
    """
    # Basic validation of the base command
    if not isinstance(base_command, str) or not base_command.strip():
        raise ValueError("base_command must be a non‑empty string")

    # Ensure parameters is a list of strings
    if not isinstance(parameters, list) or any(
        not isinstance(p, str) for p in parameters
    ):
        raise ValueError("parameters must be a list of strings")

    # Build the command arguments list
    cmd = [base_command] + parameters

    try:
        # Execute without invoking the shell to avoid injection
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,  # We handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {base_command}") from exc
    except OSError as exc:
        raise ValueError(f"Execution failed for command: {base_command}") from exc

    if result.returncode != 0:
        # Include stderr in the error message for clarity
        raise ValueError(
            f"Command '{base_command}' exited with code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout