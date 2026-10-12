import subprocess
import shlex
from typing import List


def run_command(cmd: str, cmd_arguments: List[str]) -> str:
    """
    Execute a shell command with the supplied arguments and return its output.

    Parameters
    ----------
    cmd : str
        The main executable command to run.
    cmd_arguments : list[str]
        A list of arguments that will be passed to the command.

    Returns
    -------
    str
        The combined stdout and stderr output from the executed process.

    Raises
    ------
    ValueError
        If `cmd` is not a string, if the arguments are not a list of strings,
        or if the command fails to execute (e.g., file not found, non‑zero exit
        status).
    """
    # Validate input types
    if not isinstance(cmd, str):
        raise ValueError("`cmd` must be a string representing the executable.")
    if not isinstance(cmd_arguments, list) or not all(isinstance(a, str) for a in cmd_arguments):
        raise ValueError("`cmd_arguments` must be a list of strings.")

    # Build the command list safely.  We use shlex.quote only for debugging or
    # logging purposes; subprocess handles argument quoting internally.
    command = [cmd] + cmd_arguments

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,          # Raises CalledProcessError on non‑zero exit
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd}") from exc
    except subprocess.CalledProcessError as exc:
        # Include stderr in the error message for easier debugging
        raise ValueError(
            f"Command '{cmd}' failed with exit code {exc.returncode}:\n"
            f"{exc.stderr.strip()}"
        ) from exc

    # Return the command's standard output (and optionally stderr if needed)
    return result.stdout.strip()