import subprocess
from typing import List

def run_shell_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command safely with the supplied arguments.

    Parameters
    ----------
    cmd : str
        The primary command to run.
    arguments : list[str]
        List of arguments for the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command fails to execute or returns a non‑zero exit status.
    """
    # Build the full argument list.  Using a list and ``shell=False`` ensures
    # that each component is passed literally to the executable, preventing
    # command injection vulnerabilities (CWE‑77).
    full_cmd = [cmd] + arguments

    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            check=False,          # We handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd}") from exc
    except OSError as exc:
        raise ValueError(f"Failed to execute command '{cmd}': {exc}") from exc

    if result.returncode != 0:
        # Include both stdout and stderr in the error message for easier debugging.
        raise ValueError(
            f"Command '{cmd}' failed with exit code {result.returncode}.\n"
            f"Stdout:\n{result.stdout}\nStderr:\n{result.stderr}"
        )

    return result.stdout