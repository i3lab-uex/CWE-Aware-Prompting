import subprocess
from typing import List

def run_shell_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command safely with the provided arguments and return its output.

    Parameters
    ----------
    cmd : str
        The base command to execute (e.g., "ls", "grep").
    arguments : list[str]
        A list of string arguments for the command.

    Returns
    -------
    str
        The stdout produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed or returns a non‑zero exit status.
    """
    # Build the argument list for subprocess; do not use shell=True to avoid injection.
    process_args = [cmd] + arguments

    try:
        result = subprocess.run(
            process_args,
            capture_output=True,
            text=True,
            check=False,          # We'll handle errors ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command '{cmd}' not found") from exc
    except Exception as exc:  # Catch any other subprocess-related errors
        raise ValueError(f"Failed to execute command '{cmd}': {exc}") from exc

    if result.returncode != 0:
        # Include stderr in the exception message for debugging.
        raise ValueError(
            f"Command '{cmd}' failed with exit code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout