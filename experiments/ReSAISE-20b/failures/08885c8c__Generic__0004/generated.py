import subprocess
from typing import List

def run_shell_cmd(cmd_name: str, cmd_args: List[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    cmd_name : str
        The main command to run (e.g., "ls", "echo").
    cmd_args : list
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be found, fails to execute,
        or returns a non‑zero exit status.
    """
    if not isinstance(cmd_name, str) or not cmd_name:
        raise ValueError("cmd_name must be a non‑empty string")

    if not isinstance(cmd_args, list):
        raise ValueError("cmd_args must be a list")

    # Build the command sequence; using a list keeps it safe from shell injection
    cmd_sequence = [cmd_name] + cmd_args

    try:
        result = subprocess.run(
            cmd_sequence,
            capture_output=True,
            text=True,
            check=True,  # Raises CalledProcessError on non‑zero exit
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd_name}") from exc
    except subprocess.CalledProcessError as exc:
        # Include stderr in the error message for easier debugging
        raise ValueError(
            f"Command '{cmd_name}' failed with exit code {exc.returncode}:\n{exc.stderr}"
        ) from exc
    except Exception as exc:
        # Catch-all for unexpected errors
        raise ValueError(f"Unexpected error running command '{cmd_name}': {exc}") from exc

    return result.stdout