import subprocess
import shlex
import shutil
from typing import List

def run_command(cmd: str, cmd_arguments: List[str]) -> str:
    """
    Execute a shell command with the supplied arguments and return its output.

    Parameters
    ----------
    cmd : str
        The main command to run.
    cmd_arguments : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The combined stdout and stderr output of the executed command.

    Raises
    ------
    ValueError
        If `cmd` is empty, not found in the system path,
        or if the command exits with a non‑zero status.
    """
    # Basic validation of the command string
    if not isinstance(cmd, str) or not cmd.strip():
        raise ValueError("Command must be a non‑empty string")

    # Ensure the command exists on the system
    if shutil.which(cmd) is None:
        raise ValueError(f"Command not found: {cmd}")

    # Build the full command list
    # `shlex.quote` is not required here because we pass arguments as a list,
    # but we still quote the command for safety in error messages.
    full_cmd = [cmd] + cmd_arguments

    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            check=False  # We will handle non‑zero exit codes ourselves
        )
    except Exception as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    output = result.stdout.strip() + ("\n" if result.stdout and result.stderr else "") + result.stderr.strip()

    # Raise ValueError on non‑zero exit status
    if result.returncode != 0:
        raise ValueError(f"Command '{shlex.quote(cmd)}' exited with status {result.returncode}:\n{output}")

    return output