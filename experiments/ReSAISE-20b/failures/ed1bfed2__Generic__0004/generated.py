import subprocess
from typing import List


def run_shell_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    cmd : str
        The base command to run.
    arguments : list of str
        List of arguments for the command.

    Returns
    -------
    str
        The stdout produced by the command.

    Raises
    ------
    ValueError
        If the command is invalid or fails to execute.
    """
    # Build a list suitable for subprocess.run (avoids shell=True)
    command = [cmd] + arguments

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,          # Raises CalledProcessError on non-zero exit
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd}") from exc
    except subprocess.CalledProcessError as exc:
        # Include stderr in the error message for easier debugging
        raise ValueError(
            f"Command '{cmd}' failed with exit code {exc.returncode}:\n{exc.stderr}"
        ) from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command '{cmd}': {exc}") from exc

    return result.stdout