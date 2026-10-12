import subprocess
from typing import List

def run_shell_command(shell_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    shell_command : str
        The base command to run (e.g., "ls", "grep").
    parameters : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed, is invalid, or returns a non‑zero exit status.
    """
    if not isinstance(shell_command, str):
        raise ValueError("shell_command must be a string")
    if not isinstance(parameters, list) or not all(isinstance(p, str) for p in parameters):
        raise ValueError("parameters must be a list of strings")

    # Construct the command as a list to avoid shell injection.
    cmd = [shell_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False  # We handle non‑zero status ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {shell_command}") from exc
    except OSError as exc:
        raise ValueError(f"Execution failed for command: {shell_command}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{shell_command}' exited with status {result.returncode}\n"
            f"stderr: {result.stderr.strip()}"
        )

    return result.stdout