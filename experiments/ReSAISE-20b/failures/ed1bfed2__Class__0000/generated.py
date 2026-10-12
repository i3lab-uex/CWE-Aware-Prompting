import subprocess
from typing import List


def run_shell_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    cmd : str
        The base command to execute (e.g., "ls", "python").
    arguments : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If `cmd` is not a string, if any argument is not a string,
        or if the command fails to execute (non‑zero exit status).
    """
    # Basic input validation
    if not isinstance(cmd, str):
        raise ValueError("cmd must be a string")
    if not isinstance(arguments, list) or not all(isinstance(a, str) for a in arguments):
        raise ValueError("arguments must be a list of strings")

    # Build the argument vector.  Do NOT use shell=True to avoid command injection.
    cmd_list = [cmd] + arguments

    try:
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            check=False,          # We'll handle non‑zero exit manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd}") from exc
    except OSError as exc:
        raise ValueError(f"Execution failed: {exc}") from exc

    if result.returncode != 0:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command '{cmd}' exited with status {result.returncode}:\n{result.stderr}"
        )

    return result.stdout