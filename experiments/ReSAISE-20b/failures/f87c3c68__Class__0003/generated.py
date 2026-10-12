import subprocess
import shutil
from typing import List


def run_shell_command(shell_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the supplied arguments and return its output.

    Parameters
    ----------
    shell_command : str
        The executable or command to run.
    parameters : List[str]
        A list of arguments for the command.

    Returns
    -------
    str
        The stdout output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be found or execution fails.
    """
    # Ensure the command exists on the system
    if not shutil.which(shell_command):
        raise ValueError(f"Command '{shell_command}' not found on the system.")

    # Build argument list safely – no shell=True
    cmd = [shell_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,          # decode bytes to str
            check=True          # raise CalledProcessError on non-zero exit
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command '{shell_command}' not found.") from e
    except subprocess.CalledProcessError as e:
        raise ValueError(
            f"Command '{shell_command}' failed with exit code {e.returncode}:\n"
            f"{e.stderr.strip()}"
        ) from e
    except Exception as e:
        raise ValueError(f"An unexpected error occurred while executing '{shell_command}': {e}") from e

    return result.stdout.strip()