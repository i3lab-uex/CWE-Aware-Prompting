import shlex
import subprocess
from typing import List


def run_command_with_args(base_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the supplied arguments and return its output.

    Parameters
    ----------
    base_command : str
        The primary command to run (e.g., "git", "python").
    parameters : list
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command, decoded as UTF-8.

    Raises
    ------
    ValueError
        If the command fails to start or returns a non‑zero exit status.
    """
    if not isinstance(base_command, str) or not base_command.strip():
        raise ValueError("base_command must be a non‑empty string")

    if not isinstance(parameters, list):
        raise ValueError("parameters must be a list of strings")

    # Safely construct the argument list
    cmd = [base_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,          # Automatically decode bytes to str
            check=True          # Raise CalledProcessError on non‑zero exit
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {base_command}") from exc
    except subprocess.CalledProcessError as exc:
        raise ValueError(
            f"Command '{base_command}' failed with exit code {exc.returncode}.\n"
            f"Output:\n{exc.output}"
        ) from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    return result.stdout