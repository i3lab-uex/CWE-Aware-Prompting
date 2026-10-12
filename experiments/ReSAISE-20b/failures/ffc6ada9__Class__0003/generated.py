import subprocess
import shlex
import shutil
from typing import List


def execute_command(base_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command safely and return its output.

    Parameters
    ----------
    base_command : str
        The main command to execute.
    parameters : list of str
        Arguments that will be passed to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the base command is not found, or if parameters are not a list of strings.
    """
    # Validate base_command
    if not isinstance(base_command, str) or not base_command.strip():
        raise ValueError("base_command must be a non-empty string")

    # Verify command exists in PATH
    if shutil.which(base_command) is None:
        raise ValueError(f"Command '{base_command}' not found in PATH")

    # Validate parameters
    if not isinstance(parameters, list):
        raise ValueError("parameters must be a list")
    for arg in parameters:
        if not isinstance(arg, str):
            raise ValueError("All parameters must be strings")

    # Build the command list for subprocess.run
    cmd = [base_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True  # Raises CalledProcessError on non-zero exit
        )
    except subprocess.CalledProcessError as e:
        # Return stderr for debugging but raise ValueError
        raise ValueError(
            f"Command '{base_command}' failed with exit code {e.returncode}: "
            f"{e.stderr.strip()}"
        ) from e

    return result.stdout