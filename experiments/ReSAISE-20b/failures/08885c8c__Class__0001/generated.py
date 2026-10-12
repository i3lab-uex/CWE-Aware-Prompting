import subprocess
import shlex
import shutil
from typing import List

def run_shell_cmd(cmd_name: str, cmd_args: List[str]) -> str:
    """
    Execute a shell command safely using subprocess without invoking the shell.

    Parameters
    ----------
    cmd_name : str
        The main command to run (e.g., "ls", "git").
    cmd_args : list
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command is not found, cannot be executed,
        or returns a non-zero exit status.
    """
    # Resolve the command to an absolute path to ensure it exists
    cmd_path = shutil.which(cmd_name)
    if not cmd_path:
        raise ValueError(f"Command '{cmd_name}' not found in PATH")

    # Build the full argument list
    cmd_list = [cmd_path] + cmd_args

    try:
        result = subprocess.run(
            cmd_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
            text=True  # ensures the output is returned as a string
        )
    except subprocess.CalledProcessError as exc:
        # Return the output that caused the error for debugging
        raise ValueError(
            f"Command '{cmd_name}' failed with exit code {exc.returncode}: {exc.output}"
        ) from exc
    except OSError as exc:
        raise ValueError(f"Failed to execute command '{cmd_name}': {exc}") from exc

    return result.stdout