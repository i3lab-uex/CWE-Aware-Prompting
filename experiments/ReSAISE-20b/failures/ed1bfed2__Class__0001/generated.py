import subprocess
from typing import List


def run_shell_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    cmd : str
        The base command to run (e.g., "ls", "python").
    arguments : list of str
        A list of command‑line arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the executed command.

    Raises
    ------
    ValueError
        If `cmd` is empty, any argument is not a string,
        or the command exits with a non‑zero status.
    """
    if not isinstance(cmd, str) or not cmd.strip():
        raise ValueError("`cmd` must be a non‑empty string")

    if not isinstance(arguments, list):
        raise ValueError("`arguments` must be a list")

    for arg in arguments:
        if not isinstance(arg, str):
            raise ValueError("All elements of `arguments` must be strings")

    # Build the command list; avoid using shell=True to prevent injection.
    full_cmd = [cmd] + arguments

    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            check=False  # we handle non‑zero exit codes manually
        )
    except OSError as exc:
        raise ValueError(f"Failed to execute command '{cmd}': {exc}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd}' failed with exit code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout