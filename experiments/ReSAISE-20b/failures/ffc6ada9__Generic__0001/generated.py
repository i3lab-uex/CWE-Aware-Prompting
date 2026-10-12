import subprocess
import shlex
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
        The combined stdout and stderr output of the executed command.

    Raises
    ------
    ValueError
        If `base_command` is not a string or empty, if `parameters`
        contains non‑string elements, or if the command execution fails.
    """
    # Basic validation
    if not isinstance(base_command, str) or not base_command.strip():
        raise ValueError("base_command must be a non‑empty string")

    if not isinstance(parameters, list):
        raise ValueError("parameters must be a list of strings")

    for arg in parameters:
        if not isinstance(arg, str):
            raise ValueError("all items in parameters must be strings")

    # Build the command list for subprocess
    cmd = [base_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,          # Raises CalledProcessError on non‑zero exit
        )
    except subprocess.CalledProcessError as exc:
        # Provide a clear error message that includes the command and exit code
        cmd_str = " ".join(shlex.quote(part) for part in cmd)
        raise ValueError(
            f"Command failed: {cmd_str}\nExit code: {exc.returncode}\n"
            f"Error output:\n{exc.stderr}"
        ) from exc
    except FileNotFoundError as exc:
        # Command not found on the system
        raise ValueError(f"Command not found: {base_command}") from exc

    # Return stdout (and optionally stderr if needed)
    return result.stdout.strip()