import subprocess
from typing import List

def run_command_with_args(base_command: str, parameters: List[str]) -> str:
    """
    Execute an external command safely with the given arguments.

    Parameters
    ----------
    base_command : str
        The primary command to run (e.g., 'ls', '/usr/bin/python').
    parameters : list
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output from the executed command.

    Raises
    ------
    ValueError
        If the command cannot be executed or returns a non‑zero exit status.
    """
    # Build the full argument list; do not use shell=True to avoid injection
    cmd = [base_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,          # decode bytes to str using locale encoding
            check=False,        # we handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {base_command}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command exited with non‑zero status {result.returncode}:\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )

    return result.stdout