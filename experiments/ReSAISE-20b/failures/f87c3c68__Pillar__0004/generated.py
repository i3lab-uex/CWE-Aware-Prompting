import subprocess
import shlex
from typing import List


def run_shell_command(shell_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    shell_command : str
        The base command to run (e.g., "ls", "grep").
    parameters : list
        A list of string arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output (and error if any) produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed, is not found, or returns a non‑zero exit status.
    """
    # Build the command list safely
    try:
        base_cmd = shlex.split(shell_command)
    except ValueError as exc:
        raise ValueError(f"Invalid shell command syntax: {shell_command}") from exc

    if not base_cmd:
        raise ValueError("Empty command provided")

    cmd = base_cmd + parameters

    try:
        result = subprocess.run(
            cmd,
            check=True,               # Raise CalledProcessError on non-zero exit
            capture_output=True,      # Capture stdout and stderr
            text=True,                # Return strings instead of bytes
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {base_cmd[0]}") from exc
    except subprocess.CalledProcessError as exc:
        # Combine stdout and stderr for diagnostic purposes
        output = exc.stdout or ""
        error_msg = exc.stderr or ""
        raise ValueError(
            f"Command '{' '.join(cmd)}' failed with exit code {exc.returncode}.\n"
            f"Output: {output}\nError: {error_msg}"
        ) from exc
    except Exception as exc:
        # Catch-all for unexpected errors (e.g., permission denied)
        raise ValueError(f"Failed to execute command '{' '.join(cmd)}': {exc}") from exc

    # Return the captured output (stdout + stderr if any)
    return result.stdout or result.stderr