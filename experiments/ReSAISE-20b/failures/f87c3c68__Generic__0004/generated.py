import subprocess
from typing import List


def run_shell_command(shell_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    shell_command : str
        The command to execute (e.g., 'ls', 'grep').
    parameters : list[str]
        List of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed or returns a non‑zero exit status.
    """
    # Build the argument list for subprocess.run
    cmd = [shell_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,          # Raises CalledProcessError on non-zero exit
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {shell_command}") from exc
    except subprocess.CalledProcessError as exc:
        # Provide both stdout and stderr for debugging
        err_msg = (
            f"Command '{shell_command}' failed with exit code {exc.returncode}\n"
            f"stdout: {exc.stdout}\nstderr: {exc.stderr}"
        )
        raise ValueError(err_msg) from exc
    except Exception as exc:  # Catch any other unexpected errors
        raise ValueError(f"Failed to execute command '{shell_command}': {exc}") from exc

    return result.stdout