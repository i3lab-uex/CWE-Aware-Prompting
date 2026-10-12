import subprocess
from typing import List


def execute_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the supplied arguments and return its output.

    Parameters
    ----------
    cmd : str
        The command to run (e.g., "ls", "python").
    arguments : list[str]
        List of positional arguments to pass to the command.

    Returns
    -------
    str
        Standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed or is invalid.
    """
    if not cmd:
        raise ValueError("Command must not be empty")

    # Build the argument list for subprocess.run
    cmd_list = [cmd] + arguments

    try:
        result = subprocess.run(
            cmd_list,
            check=True,               # raise CalledProcessError on non‑zero exit
            capture_output=True,      # capture stdout and stderr
            text=True                 # return strings instead of bytes
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {cmd}") from e
    except subprocess.CalledProcessError as e:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command '{cmd}' failed with exit code {e.returncode}: "
            f"{e.stderr.strip()}"
        ) from e
    except Exception as e:
        # Catch any other unexpected exception and wrap it in ValueError
        raise ValueError(f"Failed to execute command '{cmd}': {e}") from e

    return result.stdout.strip()