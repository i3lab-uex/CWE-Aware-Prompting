import subprocess
import shlex
import shutil
from typing import List


def execute_command(base_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command safely with the given arguments.

    Parameters
    ----------
    base_command : str
        The main executable to run.
    parameters : list of str
        Arguments that will be passed to the command.

    Returns
    -------
    str
        The combined stdout and stderr output from the executed command.

    Raises
    ------
    ValueError
        If the base_command cannot be found or if execution fails.
    """
    # Ensure the command exists in PATH
    cmd_path = shutil.which(base_command)
    if not cmd_path:
        raise ValueError(f"Command '{base_command}' not found in PATH.")

    # Build the full argument list
    cmd_list = [cmd_path] + parameters

    try:
        # Execute the command without invoking a shell
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            check=True,          # Raises CalledProcessError on non-zero exit
        )
    except subprocess.CalledProcessError as exc:
        # Provide meaningful error information
        raise ValueError(
            f"Command '{base_command}' failed with exit code {exc.returncode}.\n"
            f"Stdout: {exc.stdout}\nStderr: {exc.stderr}"
        ) from exc
    except OSError as exc:
        # Handles cases like permission denied, etc.
        raise ValueError(f"Execution failed: {exc}") from exc

    # Return the command output
    return result.stdout.strip()