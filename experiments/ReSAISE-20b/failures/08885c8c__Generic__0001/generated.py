import subprocess
from typing import List

def run_shell_cmd(cmd_name: str, cmd_args: List[str]) -> str:
    """
    Execute a shell command safely and return its standard output.

    Parameters
    ----------
    cmd_name : str
        The executable name or path to run.
    cmd_args : list of str
        Arguments passed to the command.

    Returns
    -------
    str
        The decoded standard output of the executed process.

    Raises
    ------
    ValueError
        If `cmd_name` is empty, not a string, or the process exits with a non‑zero
        return code.
    """
    if not isinstance(cmd_name, str) or not cmd_name:
        raise ValueError("cmd_name must be a non‑empty string")

    if not isinstance(cmd_args, list) or any(not isinstance(a, str) for a in cmd_args):
        raise ValueError("cmd_args must be a list of strings")

    # Build the command list; no shell=True for security
    cmd = [cmd_name] + cmd_args

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,          # decode bytes to str using locale encoding
            check=False         # we handle non‑zero return codes manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd_name}") from exc
    except OSError as exc:
        raise ValueError(f"Failed to execute command: {cmd_name}") from exc

    if result.returncode != 0:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command '{cmd_name}' exited with code {result.returncode}:\n{result.stderr}"
        )

    return result.stdout