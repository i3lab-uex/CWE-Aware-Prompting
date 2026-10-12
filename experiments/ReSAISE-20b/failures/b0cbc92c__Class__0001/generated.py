import subprocess
from typing import List

def run_command(cmd: str, cmd_arguments: List[str]) -> str:
    """
    Execute a shell command safely using subprocess.

    Parameters
    ----------
    cmd : str
        The main executable or command name.
    cmd_arguments : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output of the executed command.

    Raises
    ------
    ValueError
        If `cmd` is empty, not a string, or the command execution fails.
    """
    if not isinstance(cmd, str) or not cmd.strip():
        raise ValueError("Command must be a non‑empty string")

    if not isinstance(cmd_arguments, list):
        raise ValueError("cmd_arguments must be a list")

    # Build the full command as a list for subprocess (no shell expansion)
    full_cmd = [cmd] + cmd_arguments

    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,           # Decode bytes to str automatically
            check=True,          # Raise CalledProcessError on non‑zero exit code
        )
    except subprocess.CalledProcessError as exc:
        # Provide a clear error message without leaking raw shell output
        raise ValueError(
            f"Command '{cmd}' failed with exit code {exc.returncode}"
        ) from exc
    except FileNotFoundError as exc:
        raise ValueError(f"Command '{cmd}' not found") from exc

    return result.stdout