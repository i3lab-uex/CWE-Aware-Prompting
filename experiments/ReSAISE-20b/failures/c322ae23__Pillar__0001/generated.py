import subprocess
from typing import List

def run_command_with_args(base_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the supplied arguments and return its output.

    Parameters
    ----------
    base_command : str
        The primary command to run (e.g., 'ls', '/usr/bin/grep').
    parameters : list[str]
        A list of arguments for the command. Each item must be a string.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command fails to execute or returns a non‑zero exit status.
    """
    if not isinstance(base_command, str):
        raise ValueError("base_command must be a string")
    if not isinstance(parameters, list) or not all(isinstance(p, str) for p in parameters):
        raise ValueError("parameters must be a list of strings")

    # Build the command as a list; this bypasses the shell and prevents
    # injection vulnerabilities.
    cmd = [base_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False  # we handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {base_command}") from exc
    except OSError as exc:
        raise ValueError(f"Execution failed for {base_command}: {exc}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{base_command}' exited with status {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout