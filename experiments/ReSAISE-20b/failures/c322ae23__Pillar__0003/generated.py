import shlex
import subprocess
import shutil
from typing import List


def run_command_with_args(base_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the supplied arguments and return its output.

    Parameters
    ----------
    base_command : str
        The primary command to run (e.g., "ls", "/usr/bin/grep").
    parameters : list
        A list of arguments to pass to the command. Each element must be a string.

    Returns
    -------
    str
        The combined stdout and stderr output from the executed command, decoded as UTF‑8.

    Raises
    ------
    ValueError
        If the command is not found, if any argument is not a string,
        or if the subprocess exits with a non‑zero status.
    """
    # Validate input types
    if not isinstance(base_command, str):
        raise ValueError("base_command must be a string")

    if not isinstance(parameters, list) or any(not isinstance(p, str) for p in parameters):
        raise ValueError("parameters must be a list of strings")

    # Ensure the base command exists on the system
    if shutil.which(base_command) is None:
        raise ValueError(f"Command '{base_command}' not found in PATH")

    # Construct the full command list
    cmd = [base_command] + parameters

    try:
        # Execute the command, capture output, raise on error
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,  # decode bytes to str using default encoding (utf-8)
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        # The command exited with a non-zero status
        raise ValueError(
            f"Command '{base_command}' failed with exit code {exc.returncode}\n"
            f"Output:\n{exc.output}"
        ) from exc
    except Exception as exc:
        # Any other exception (e.g., OSError) is wrapped in ValueError
        raise ValueError(f"Failed to execute command '{base_command}': {exc}") from exc

    return result.stdout