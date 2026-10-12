import subprocess
import shlex
from typing import List


def run_shell_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    cmd : str
        The base command to execute.
    arguments : list of str
        A list containing the arguments for the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command fails to execute or returns a non-zero exit status.
    """
    # Construct the full command list safely (no shell=True)
    command = [cmd] + arguments

    try:
        # Run the command, capture output, and enforce UTF‑8 decoding
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
    except FileNotFoundError as exc:
        # The command binary was not found
        raise ValueError(f"Command not found: {shlex.quote(cmd)}") from exc
    except subprocess.CalledProcessError as exc:
        # The command executed but returned a non-zero exit status
        raise ValueError(
            f"Command failed with exit code {exc.returncode}:\n{exc.output}"
        ) from exc
    except Exception as exc:
        # Catch any other unexpected errors
        raise ValueError(f"An error occurred while executing the command: {exc}") from exc

    return result.stdout