import subprocess
from typing import List


def run_shell_cmd(cmd_name: str, cmd_args: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    cmd_name : str
        The executable to run.
    cmd_args : list of str
        Arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If `cmd_name` is empty, not a string, or the command cannot be executed.
    """
    # Basic validation
    if not isinstance(cmd_name, str) or not cmd_name.strip():
        raise ValueError("cmd_name must be a non‑empty string")

    if not isinstance(cmd_args, list) or not all(isinstance(a, str) for a in cmd_args):
        raise ValueError("cmd_args must be a list of strings")

    # Build the command list; do not use shell=True to avoid injection risks
    cmd = [cmd_name] + cmd_args

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,          # decoded to str
            check=True,         # raise CalledProcessError on non‑zero exit
        )
    except FileNotFoundError as e:
        # Command does not exist on the system
        raise ValueError(f"Command '{cmd_name}' not found") from e
    except subprocess.CalledProcessError as e:
        # Non‑zero exit status – treat as an error
        raise ValueError(
            f"Command '{cmd_name}' failed with exit code {e.returncode}: "
            f"{e.stderr.strip()}"
        ) from e
    except Exception as e:
        # Catch-all for unexpected errors
        raise ValueError(f"Failed to execute command '{cmd_name}': {e}") from e

    return result.stdout