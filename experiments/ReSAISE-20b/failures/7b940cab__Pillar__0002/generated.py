import subprocess
from typing import List


def execute_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the supplied arguments and return its output.

    Parameters
    ----------
    cmd : str
        The command to execute (e.g., "ls", "python").
    arguments : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed, if it exits with a non‑zero status,
        or if input types are invalid.
    """
    # Basic type validation
    if not isinstance(cmd, str):
        raise ValueError("`cmd` must be a string.")
    if not isinstance(arguments, list) or not all(isinstance(a, str) for a in arguments):
        raise ValueError("`arguments` must be a list of strings.")

    # Build the command line
    full_cmd = [cmd] + arguments

    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,          # decode bytes to str
            check=False,        # we handle errors manually
            shell=False         # prevent shell injection
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {cmd}") from e
    except Exception as e:
        raise ValueError(f"Failed to execute command: {cmd}") from e

    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd}' exited with status {result.returncode}.\n"
            f"Stderr: {result.stderr.strip()}"
        )

    return result.stdout.strip()