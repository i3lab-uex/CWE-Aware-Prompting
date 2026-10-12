import subprocess
import shlex
from typing import List

def execute_command(base_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the supplied arguments and return its output.

    Parameters
    ----------
    base_command : str
        The main command to execute.  It may contain the program name and any
        options that should be treated as part of the command itself.
    parameters : List[str]
        A list of arguments to pass after the base command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be parsed, or if execution fails (non‑zero exit
        status).  The error message contains the command and its return code.
    """
    # Split the base_command into a list of tokens safely
    try:
        cmd_parts = shlex.split(base_command)
    except ValueError as exc:   # shlex raises ValueError on malformed input
        raise ValueError(f"Invalid base command: {base_command}") from exc

    # Combine with user supplied parameters
    full_cmd = cmd_parts + list(parameters)

    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,          # decode bytes to str
            check=False         # we handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {full_cmd[0]}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command: {full_cmd}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{' '.join(full_cmd)}' failed with exit code "
            f"{result.returncode}\nStderr: {result.stderr}"
        )

    return result.stdout