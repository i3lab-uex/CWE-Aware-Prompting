import subprocess
import shlex
from shutil import which
from typing import List


def run_shell_cmd(cmd_name: str, cmd_args: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    cmd_name : str
        The executable to run (e.g., 'ls', 'git').
    cmd_args : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command, decoded as UTF‑8.

    Raises
    ------
    ValueError
        If the command is not found, cannot be executed, or exits with a non‑zero status.
    """
    # Verify that the command exists in PATH
    if which(cmd_name) is None:
        raise ValueError(f"Command not found: {cmd_name}")

    # Build the full command list
    cmd = [cmd_name] + cmd_args

    try:
        # Run the command without invoking a shell to avoid injection issues.
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,  # decode bytes to str using locale encoding
            check=True,  # raise CalledProcessError on non-zero exit
        )
    except subprocess.CalledProcessError as exc:
        # Provide a clear error message while preserving the original output
        raise ValueError(
            f"Command '{shlex.join(cmd)}' failed with exit code {exc.returncode}.\n"
            f"Stdout: {exc.stdout}\nStderr: {exc.stderr}"
        ) from exc
    except OSError as exc:
        # Covers cases like permission denied, file not executable, etc.
        raise ValueError(f"Execution failed for '{cmd_name}': {exc}") from exc

    # Return the command's stdout (stderr is omitted by design)
    return result.stdout