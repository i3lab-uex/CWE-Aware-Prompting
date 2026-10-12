import subprocess
from typing import List


def run_command_with_args(base_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    base_command : str
        The primary command to run (e.g., 'ls', 'git').
    parameters : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command is invalid, fails to execute, or returns a non‑zero exit status.
    """
    if not isinstance(base_command, str) or not base_command:
        raise ValueError("`base_command` must be a non‑empty string")

    if not isinstance(parameters, list):
        raise ValueError("`parameters` must be a list")

    # Construct the command as a list to avoid shell injection
    cmd = [base_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,          # Raises CalledProcessError on non‑zero exit
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {base_command}") from e
    except subprocess.CalledProcessError as e:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command '{base_command}' failed with exit code {e.returncode}:\n{e.stderr}"
        ) from e
    except Exception as e:
        # Catch any other unexpected errors
        raise ValueError(f"An error occurred while running '{base_command}': {e}") from e

    return result.stdout