import shlex
import subprocess
from typing import List


def run_shell_command(shell_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    shell_command : str
        The command to run (e.g., "ls" or "/usr/bin/grep").
    parameters : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed or returns a non‑zero exit status.
    """
    # Safely split the command string into a list of tokens
    cmd_tokens = shlex.split(shell_command)

    # Combine command and parameters into a single list
    full_cmd = cmd_tokens + parameters

    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            check=False,  # We will handle non‑zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {shell_command}") from exc
    except PermissionError as exc:
        raise ValueError(f"Permission denied for command: {shell_command}") from exc
    except OSError as exc:
        raise ValueError(f"Failed to execute command: {shell_command}") from exc

    if result.returncode != 0:
        err_msg = (
            f"Command '{' '.join(full_cmd)}' exited with status {result.returncode}.\n"
            f"stderr: {result.stderr.strip()}"
        )
        raise ValueError(err_msg)

    return result.stdout