import subprocess
import shlex
from typing import List

def run_command_with_args(base_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the supplied arguments and return its output.

    Parameters
    ----------
    base_command : str
        The primary command to run (e.g. "ls", "git").
    parameters : list
        A list of string arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If `base_command` is not a string, if any parameter is not a string,
        or if the command fails to execute.
    """
    # Basic validation
    if not isinstance(base_command, str):
        raise ValueError("base_command must be a string")
    if not isinstance(parameters, list) or any(
        not isinstance(p, str) for p in parameters
    ):
        raise ValueError("parameters must be a list of strings")

    # Build the command as a list for subprocess.run (no shell expansion)
    cmd = [base_command] + parameters

    try:
        # Execute the command, capture stdout and stderr
        result = subprocess.run(
            cmd,
            check=True,
            text=True,          # Return strings instead of bytes
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Combine stderr into stdout
        )
        return result.stdout.strip()
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {base_command}") from e
    except subprocess.CalledProcessError as e:
        # The command exited with a non-zero status
        raise ValueError(
            f"Command '{base_command}' failed with exit code {e.returncode}\n"
            f"Output: {e.output}"
        ) from e
    except Exception as e:
        # Catch any other unexpected errors
        raise ValueError(f"Failed to execute command '{base_command}': {e}") from e