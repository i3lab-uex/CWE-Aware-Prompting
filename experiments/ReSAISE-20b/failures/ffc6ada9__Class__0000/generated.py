import subprocess
import shlex
import shutil
from typing import List


def execute_command(base_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the given parameters and return its output.

    Parameters
    ----------
    base_command : str
        The main command to run (e.g., 'ls', 'git', etc.).
    parameters : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output produced by the command.

    Raises
    ------
    ValueError
        If the base_command is not found in the system PATH, if any argument
        cannot be safely parsed, or if the command exits with a non‑zero status.
    """
    # Ensure the base command exists in PATH
    if shutil.which(base_command) is None:
        raise ValueError(f"Command '{base_command}' not found in PATH")

    # Build the command list.  Each element is already a safe string.
    cmd = [base_command] + parameters

    try:
        # Run the command without using a shell to avoid injection.
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,  # decode bytes to str using locale encoding
            check=False,  # we handle non‑zero exit below
        )
    except OSError as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    # If the command failed, raise an error with stderr information
    if result.returncode != 0:
        raise ValueError(
            f"Command '{base_command}' failed with exit code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout.strip()