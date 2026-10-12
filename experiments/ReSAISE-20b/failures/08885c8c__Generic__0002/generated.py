import subprocess
from typing import List

def run_shell_cmd(cmd_name: str, cmd_args: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    cmd_name : str
        The main command to run (e.g., 'ls', 'grep').
    cmd_args : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If `cmd_name` is empty, not a string, if any argument is not a string,
        or if the command fails to execute (non-zero exit status).
    """
    # Basic validation
    if not isinstance(cmd_name, str) or not cmd_name.strip():
        raise ValueError("cmd_name must be a non‑empty string")
    if not isinstance(cmd_args, list) or any(
        not isinstance(arg, str) for arg in cmd_args
    ):
        raise ValueError("cmd_args must be a list of strings")

    # Build the command
    cmd = [cmd_name] + cmd_args

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,          # We'll handle errors ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd_name}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd_name}' failed with exit code {result.returncode}\n"
            f"stderr: {result.stderr.strip()}"
        )

    return result.stdout