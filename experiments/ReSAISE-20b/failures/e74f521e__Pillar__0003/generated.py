import subprocess
import shlex
import shutil
from typing import List


def run_shell_cmd(cmd: str, params: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    cmd : str
        The command to run (e.g., 'ls', 'grep').
    params : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The stdout produced by the command. If the command writes to stderr,
        it will be captured as part of stdout.

    Raises
    ------
    ValueError
        If the command is not found, if any argument is not a string,
        or if the command exits with a non‑zero return code.
    """
    # Validate input types
    if not isinstance(cmd, str):
        raise ValueError("cmd must be a string")
    if not isinstance(params, list) or any(not isinstance(p, str) for p in params):
        raise ValueError("params must be a list of strings")

    # Ensure the command exists on the system
    if shutil.which(cmd) is None:
        raise ValueError(f"Command '{cmd}' not found in PATH")

    # Build the argument list for subprocess.run
    # Using a list prevents shell injection and avoids the need to quote manually.
    full_cmd = [cmd] + params

    try:
        # Execute the command without invoking a shell
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,          # return string instead of bytes
            check=False         # we'll handle non‑zero exit ourselves
        )
    except OSError as e:
        # Raised if the command cannot be executed at all
        raise ValueError(f"Failed to execute '{cmd}': {e}") from e

    # If the command failed, raise an error with useful information
    if result.returncode != 0:
        err_msg = (
            f"Command '{cmd}' exited with status {result.returncode}\n"
            f"Stdout: {result.stdout.strip()}\n"
            f"Stderr: {result.stderr.strip()}"
        )
        raise ValueError(err_msg)

    # Return the command's stdout (stripped of trailing newlines for cleanliness)
    return result.stdout.strip()