import subprocess
import shlex
from shutil import which
from typing import List


def execute_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    cmd : str
        The command to run. Must be a valid executable in the system PATH.
    arguments : list
        A list of strings representing command‑line arguments.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command is not found, or if execution fails.
    """
    # Ensure that the base command exists to avoid injection via a non‑existent path
    if which(cmd) is None:
        raise ValueError(f"Command not found: {cmd}")

    # Build the full argument list.  Using a list and avoiding shell=True
    # prevents interpretation of special characters by the shell.
    cmd_list = [cmd] + arguments

    try:
        # Capture stdout and stderr; raise on non‑zero exit codes
        result = subprocess.run(
            cmd_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
            text=True,          # Decode bytes to str using locale encoding
        )
    except subprocess.CalledProcessError as exc:
        # Provide the command output in the exception message for debugging
        raise ValueError(
            f"Command '{cmd}' failed with exit code {exc.returncode}. "
            f"Output: {exc.output}"
        ) from exc
    except FileNotFoundError as exc:
        # This should not happen because we checked with shutil.which
        raise ValueError(f"Command not found: {cmd}") from exc

    return result.stdout