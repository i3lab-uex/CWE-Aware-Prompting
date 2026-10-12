import subprocess
import shlex
import shutil
from typing import List

def run_shell_cmd(cmd_name: str, cmd_args: List[str]) -> str:
    """
    Execute a shell command safely and return its output.

    Parameters
    ----------
    cmd_name : str
        The executable to run.
    cmd_args : list[str]
        List of arguments for the command.

    Returns
    -------
    str
        Standard output from the executed command.

    Raises
    ------
    ValueError
        If the command cannot be found or execution fails.
    """
    # Verify that the command exists in PATH
    executable = shutil.which(cmd_name)
    if not executable:
        raise ValueError(f"Command '{cmd_name}' not found in PATH")

    # Build the command list.  Using a list ensures no shell expansion.
    cmd = [executable] + cmd_args

    try:
        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,          # returns string instead of bytes
        )
    except subprocess.CalledProcessError as exc:
        raise ValueError(
            f"Command '{cmd_name}' failed with exit code {exc.returncode}\n"
            f"Output: {exc.output}"
        ) from exc
    except OSError as exc:
        raise ValueError(f"Failed to execute command '{cmd_name}': {exc}") from exc

    return result.stdout