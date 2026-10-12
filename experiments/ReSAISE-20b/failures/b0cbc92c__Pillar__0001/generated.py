import subprocess
from typing import List

def run_command(cmd: str, cmd_arguments: List[str]) -> str:
    """
    Execute a shell command safely and return its output.

    Parameters
    ----------
    cmd : str
        The main executable or command to run.
    cmd_arguments : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If `cmd` is empty, not a string, or if the command exits with a non‑zero status.
    """
    # Basic validation
    if not isinstance(cmd, str) or not cmd.strip():
        raise ValueError("Command must be a non‑empty string")

    if not isinstance(cmd_arguments, list):
        raise ValueError("Arguments must be provided as a list")

    # Ensure all arguments are strings
    for arg in cmd_arguments:
        if not isinstance(arg, str):
            raise ValueError("All command arguments must be strings")

    # Build the full command list
    full_cmd = [cmd.strip()] + [arg.strip() for arg in cmd_arguments]

    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            check=False,          # We'll handle non‑zero exit codes ourselves
        )
    except OSError as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd}' failed with exit code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout.strip()