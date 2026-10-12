import subprocess
import shlex
from shutil import which
from typing import List

def run_command(cmd: str, cmd_arguments: List[str]) -> str:
    """
    Execute a shell command with the supplied arguments and return its output.

    Parameters
    ----------
    cmd : str
        The main executable to run (e.g., "ls", "git").
    cmd_arguments : list
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The stdout produced by the command. If the command writes to stderr,
        it is captured and returned as part of the output.

    Raises
    ------
    ValueError
        If `cmd` is empty, not found in the system PATH,
        or if execution fails for any reason.
    """
    # Basic validation of the command
    if not isinstance(cmd, str) or not cmd.strip():
        raise ValueError("Command must be a non‑empty string.")

    # Ensure the command exists in PATH
    if which(cmd) is None:
        raise ValueError(f"Command '{cmd}' not found in system PATH.")

    # Validate arguments list
    if not isinstance(cmd_arguments, list):
        raise ValueError("cmd_arguments must be a list.")
    for arg in cmd_arguments:
        if not isinstance(arg, str):
            raise ValueError("All command arguments must be strings.")

    # Build the command list; no shell expansion to avoid injection
    full_cmd = [cmd] + cmd_arguments

    try:
        # Run the command, capture both stdout and stderr
        result = subprocess.run(
            full_cmd,
            check=True,
            text=True,          # Automatically decode bytes to str
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT  # Merge stderr into stdout for simplicity
        )
    except subprocess.CalledProcessError as exc:
        # The command exited with a non‑zero status
        raise ValueError(
            f"Command '{cmd}' failed with exit code {exc.returncode}.\n"
            f"Output: {exc.output}"
        ) from exc
    except FileNotFoundError as exc:
        # This should not happen because we checked with `which`, but guard anyway
        raise ValueError(f"Command '{cmd}' not found.") from exc
    except Exception as exc:
        # Catch any other unexpected exceptions
        raise ValueError(f"Failed to execute command '{cmd}': {exc}") from exc

    return result.stdout