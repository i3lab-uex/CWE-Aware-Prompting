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
        The base command to execute.
    params : list[str]
        List of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command is invalid, cannot be found, or execution fails.
    """
    # Validate the base command
    if not isinstance(cmd, str) or not cmd.strip():
        raise ValueError("Command must be a non-empty string")

    # Ensure the command exists in PATH
    if shutil.which(cmd) is None:
        raise ValueError(f"Command '{cmd}' not found in PATH")

    # Ensure params is a list of strings
    if not isinstance(params, list) or not all(isinstance(p, str) for p in params):
        raise ValueError("Params must be a list of strings")

    # Build the argument list safely
    args = [cmd] + params

    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False,          # We'll handle non-zero exit ourselves
            shell=False           # Avoid shell injection risks
        )
    except OSError as exc:
        raise ValueError(f"Failed to execute command '{cmd}': {exc}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd}' exited with code {result.returncode}:\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )

    return result.stdout