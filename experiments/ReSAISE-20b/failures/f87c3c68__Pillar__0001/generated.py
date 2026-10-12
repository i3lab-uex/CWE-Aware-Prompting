import subprocess
import shlex
from shutil import which
from typing import List

def run_shell_command(shell_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    shell_command : str
        The base command to execute (e.g., "ls", "git").
    parameters : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be found, or if execution fails.
    """
    # Ensure the base command exists on the system
    if which(shell_command) is None:
        raise ValueError(f"Command '{shell_command}' not found on this system.")

    # Build the argument list for subprocess.run
    cmd = [shell_command] + parameters

    try:
        # Run the command without invoking a shell (safer)
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,          # decode bytes to str automatically
            check=False         # we'll handle errors ourselves
        )
    except OSError as exc:
        raise ValueError(f"Failed to execute command '{shell_command}': {exc}") from exc

    # If the process exited with a non-zero status, treat it as an error
    if result.returncode != 0:
        raise ValueError(
            f"Command '{shell_command}' exited with status {result.returncode}.\n"
            f"Stderr: {result.stderr.strip()}"
        )

    # Return the captured stdout
    return result.stdout.strip()