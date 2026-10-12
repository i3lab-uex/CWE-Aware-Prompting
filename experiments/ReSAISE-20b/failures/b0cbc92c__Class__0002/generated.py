import subprocess
import shlex
import shutil
from typing import List


def run_command(cmd: str, cmd_arguments: List[str]) -> str:
    """
    Execute a shell command with the given arguments safely.

    Parameters
    ----------
    cmd : str
        The main executable command.
    cmd_arguments : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output of the executed command.

    Raises
    ------
    ValueError
        If the executable cannot be found or if the command fails.
    """
    # Ensure the command exists in PATH
    executable = shutil.which(cmd)
    if not executable:
        raise ValueError(f"Command '{cmd}' not found in PATH")

    # Build the full command list; avoid shell=True for security
    full_cmd = [executable] + cmd_arguments

    try:
        # Execute the command, capture output
        result = subprocess.run(
            full_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,          # decode bytes to str
            check=False         # we handle errors manually
        )
    except OSError as e:
        raise ValueError(f"Execution failed: {e}") from e

    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd}' exited with code {result.returncode}:\n{result.stdout}"
        )

    return result.stdout