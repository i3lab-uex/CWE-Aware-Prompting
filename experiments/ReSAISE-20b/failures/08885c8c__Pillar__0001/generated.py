import subprocess
from typing import List

def run_shell_cmd(cmd_name: str, cmd_args: List[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    cmd_name : str
        The main command to execute (e.g., "ls", "git").
    cmd_args : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded stdout from the executed command.

    Raises
    ------
    ValueError
        If the command name is not a non‑empty string or if execution fails.
    """
    # Validate input
    if not isinstance(cmd_name, str) or not cmd_name.strip():
        raise ValueError("cmd_name must be a non‑empty string")

    if not isinstance(cmd_args, list):
        raise ValueError("cmd_args must be a list")

    # Build the full command
    cmd = [cmd_name] + cmd_args

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,          # Raises CalledProcessError on non‑zero exit
        )
    except subprocess.CalledProcessError as exc:
        # Provide a clear error message while preserving the original output
        raise ValueError(
            f"Command '{cmd_name}' failed with exit code {exc.returncode}:\n{exc.stderr}"
        ) from exc
    except FileNotFoundError as exc:
        raise ValueError(f"Command '{cmd_name}' not found") from exc
    except Exception as exc:
        raise ValueError(f"Failed to run command '{cmd_name}': {exc}") from exc

    return result.stdout