import subprocess
import shlex
from typing import List

def run_shell_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    cmd : str
        The base command to run (e.g., "ls", "git").
    arguments : List[str]
        A list of string arguments to pass to the command.

    Returns
    -------
    str
        The combined stdout and stderr output of the executed command.

    Raises
    ------
    ValueError
        If the command fails to execute or returns a non‑zero exit status.
    """
    # Build the full command list
    # The first element is the command itself, followed by arguments.
    full_cmd = [cmd] + arguments

    try:
        # Run the command without invoking a shell to avoid injection issues.
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            check=False,          # We'll handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {shlex.quote(cmd)}") from exc
    except Exception as exc:
        # Catch any other exception that might arise during execution.
        raise ValueError(f"Failed to execute command {shlex.quote(cmd)}: {exc}") from exc

    # If the process exited with a non‑zero status, treat it as an error.
    if result.returncode != 0:
        raise ValueError(
            f"Command {shlex.quote(cmd)} failed with exit code "
            f"{result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"
        )

    # Return the combined output (stdout + stderr) as a single string.
    return result.stdout + result.stderr