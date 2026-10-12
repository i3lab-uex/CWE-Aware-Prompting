import subprocess
from typing import List

def run_shell_cmd(cmd: str, params: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    cmd : str
        The command to execute (e.g., "ls", "python").
    params : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output of the command.

    Raises
    ------
    ValueError
        If the command cannot be executed, is invalid, or returns a non‑zero exit code.
    """
    if not isinstance(cmd, str) or not cmd.strip():
        raise ValueError("Command must be a non‑empty string.")

    if not isinstance(params, list):
        raise ValueError("Params must be a list of strings.")

    # Ensure all params are strings
    for p in params:
        if not isinstance(p, str):
            raise ValueError("All parameters must be strings.")

    # Build the command list; do not use shell=True for security
    command = [cmd] + params

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,          # returns strings instead of bytes
            check=False         # we'll handle non‑zero exit codes manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd}") from exc
    except OSError as exc:
        raise ValueError(f"Execution failed for command: {cmd}") from exc

    if result.returncode != 0:
        # Include stderr in the error message for debugging
        err_msg = result.stderr.strip() or "Unknown error"
        raise ValueError(f"Command '{cmd}' exited with code {result.returncode}: {err_msg}")

    return result.stdout.strip()