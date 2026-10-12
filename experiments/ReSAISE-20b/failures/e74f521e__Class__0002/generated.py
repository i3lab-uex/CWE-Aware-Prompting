import subprocess
from typing import List


def run_shell_cmd(cmd: str, params: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    cmd : str
        The base command to run (e.g., "ls", "echo").
    params : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The stdout output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed or is invalid.
    """
    # Build a list suitable for subprocess.run
    command = [cmd] + params

    try:
        # Use shell=False to avoid shell injection vulnerabilities
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,          # Decode bytes to str automatically
            check=False         # We'll handle errors ourselves
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {cmd}") from e
    except OSError as e:
        raise ValueError(f"Failed to execute command '{cmd}': {e}") from e

    # If the process exited with a non-zero status, treat it as an error
    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd}' failed with exit code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout.strip()