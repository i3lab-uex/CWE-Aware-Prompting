import subprocess
import shlex
import shutil
from typing import List


def run_shell_command(shell_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the given list of arguments and return its output.

    Parameters
    ----------
    shell_command : str
        The base command to execute (e.g., "ls", "git").
    parameters : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The combined stdout and stderr output of the executed command.

    Raises
    ------
    ValueError
        If the command cannot be found, is not executable, or if execution fails.
    """
    # Resolve the absolute path of the command to guard against shell injection
    cmd_path = shutil.which(shell_command)
    if not cmd_path:
        raise ValueError(f"Command '{shell_command}' not found or is not executable.")

    # Build the argument list safely
    args = [cmd_path] + parameters

    try:
        # Run the command without invoking a shell to avoid injection
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False,  # we handle errors manually
        )
    except Exception as exc:
        raise ValueError(f"Failed to execute command '{shell_command}': {exc}") from exc

    # Combine stdout and stderr for easier consumption
    output = result.stdout + result.stderr

    if result.returncode != 0:
        raise ValueError(
            f"Command '{shell_command}' exited with status {result.returncode}:\n{output}"
        )

    return output