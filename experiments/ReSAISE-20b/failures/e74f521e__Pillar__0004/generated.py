import subprocess
import shlex
from shutil import which

def run_shell_cmd(cmd: str, params: list) -> str:
    """
    Execute a shell command with the supplied arguments and return its output.

    Parameters
    ----------
    cmd : str
        The base command to run (e.g., 'ls', 'git').
    params : list
        List of arguments to pass to the command.

    Returns
    -------
    str
        The stdout output from the executed command.

    Raises
    ------
    ValueError
        If the command is not found, cannot be executed,
        or returns a non‑zero exit status.
    """
    # Ensure the command exists and is executable
    if not which(cmd):
        raise ValueError(f"Command '{cmd}' not found or is not executable.")

    # Build the full command list: cmd followed by its arguments
    # Using shlex.quote for each param is unnecessary here because we pass a list to subprocess.
    full_cmd = [cmd] + params

    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            check=False,      # we handle errors manually
        )
    except OSError as exc:
        raise ValueError(f"Execution failed for command '{cmd}': {exc}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd}' exited with status {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout