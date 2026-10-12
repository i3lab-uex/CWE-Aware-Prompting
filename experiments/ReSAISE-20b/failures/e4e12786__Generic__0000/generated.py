import subprocess
from typing import List

def execute_shell_command(command: str, args: List[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    command : str
        The base command to execute (e.g., "ls", "grep").
    args : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command is invalid, cannot be executed, or returns a non‑zero exit status.
    """
    if not command:
        raise ValueError("Command must be a non-empty string")

    # Build the full argument list.  Do not use shell=True to avoid shell injection.
    cmd = [command] + args

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,  # We will handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {command}") from exc
    except OSError as exc:
        raise ValueError(f"Execution failed for command '{command}': {exc}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{command}' exited with code {result.returncode}.\n"
            f"Stderr: {result.stderr.strip()}"
        )

    return result.stdout