import subprocess
from typing import List

def run_shell_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command safely and return its output.

    Parameters
    ----------
    cmd : str
        The primary executable to run (e.g., "ls", "/usr/bin/grep").
    arguments : list
        A list of string arguments for the command.

    Returns
    -------
    str
        The stdout output from the executed command.

    Raises
    ------
    ValueError
        If the command fails to execute or returns a non‑zero exit status.
    """
    # Validate inputs
    if not isinstance(cmd, str):
        raise ValueError("`cmd` must be a string.")
    if not isinstance(arguments, list) or not all(isinstance(a, str) for a in arguments):
        raise ValueError("`arguments` must be a list of strings.")

    # Construct the argument list; do not use shell=True for security
    full_cmd = [cmd] + arguments

    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            check=True,          # Raises CalledProcessError on non‑zero exit
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd}") from exc
    except subprocess.CalledProcessError as exc:
        # Include stderr in the error message for debugging
        err_msg = f"Command '{cmd}' failed with exit code {exc.returncode}:\n{exc.stderr}"
        raise ValueError(err_msg) from exc
    except Exception as exc:  # Catch-all for unforeseen issues
        raise ValueError(f"Unexpected error running command '{cmd}': {exc}") from exc

    return result.stdout