import subprocess
from typing import List


def execute_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the given list of arguments and return its output.

    Parameters
    ----------
    cmd : str
        The base command to execute (e.g., "ls", "git").
    arguments : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The combined stdout and stderr output from the command execution.

    Raises
    ------
    ValueError
        If `cmd` is empty or if the command fails to execute.
    """
    if not cmd:
        raise ValueError("Command string cannot be empty")

    # Build the command list.  Avoid using shell=True to mitigate injection risks.
    command = [cmd] + arguments

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,  # Raises CalledProcessError on non‑zero exit status
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd}") from exc
    except subprocess.CalledProcessError as exc:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command '{cmd}' failed with exit code {exc.returncode}:\n{exc.stderr}"
        ) from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command '{cmd}': {exc}") from exc

    # Return stdout; if you want stderr as well, concatenate result.stderr
    return result.stdout.strip()