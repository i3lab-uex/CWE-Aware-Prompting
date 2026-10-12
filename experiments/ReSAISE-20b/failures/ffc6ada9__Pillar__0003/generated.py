import subprocess
import shlex
import shutil
from typing import List


def execute_command(base_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    base_command : str
        The executable to run.
    parameters : list of str
        Arguments that will be passed to the executable.

    Returns
    -------
    str
        The decoded standard output of the command.

    Raises
    ------
    ValueError
        If `base_command` is empty, not found in the system PATH,
        or if any element of `parameters` is not a string.
        Also raised when the command exits with a non‑zero status code.
    """
    # Basic validation
    if not isinstance(base_command, str) or not base_command.strip():
        raise ValueError("base_command must be a non‑empty string")

    if not isinstance(parameters, list):
        raise ValueError("parameters must be a list of strings")

    for arg in parameters:
        if not isinstance(arg, str):
            raise ValueError("all elements of parameters must be strings")

    # Ensure the command exists and is executable
    cmd_path = shutil.which(base_command)
    if cmd_path is None:
        raise ValueError(f"Command '{base_command}' not found in PATH")

    # Build the command list. Using shlex.quote is unnecessary here
    # because we avoid shell=True and pass arguments as a list.
    cmd = [cmd_path] + parameters

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,  # Raises CalledProcessError on non-zero exit
        )
    except subprocess.CalledProcessError as exc:
        # Include the output in the error message for debugging
        raise ValueError(
            f"Command '{base_command}' failed with exit code {exc.returncode}:\n{exc.output.decode(errors='replace')}"
        ) from exc
    except Exception as exc:
        # Catch any other unexpected exception and wrap it
        raise ValueError(f"Failed to execute command: {exc}") from exc

    return result.stdout.decode(errors='replace')