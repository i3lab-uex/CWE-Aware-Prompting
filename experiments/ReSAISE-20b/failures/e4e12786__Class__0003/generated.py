import subprocess
import shlex
import shutil
from typing import List

def execute_shell_command(command: str, args: List[str]) -> str:
    """
    Execute a shell command safely using the provided arguments.

    Parameters
    ----------
    command : str
        The base command to execute (e.g., "ls", "git").
    args : list
        A list of arguments for the command. Each argument is passed as a separate element.

    Returns
    -------
    str
        The combined stdout and stderr output of the executed command, decoded as UTF-8.

    Raises
    ------
    ValueError
        If the command is not found, if the arguments contain shell metacharacters that
        could lead to injection when passed as a single string, or if the command fails
        to execute.
    """
    # Verify that the base command exists in PATH
    if shutil.which(command) is None:
        raise ValueError(f"Command '{command}' not found in PATH")

    # Ensure no argument contains shell metacharacters that could be interpreted
    # when passed to a single string. We treat each argument separately, so this
    # check is mainly defensive.
    for arg in args:
        if any(c in arg for c in (";", "&", "|", "$", "`", ">", "<")):
            raise ValueError(f"Argument '{arg}' contains forbidden shell metacharacters")

    # Construct the command list
    cmd_list = [command] + args

    try:
        result = subprocess.run(
            cmd_list,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,          # decode using locale's encoding (default UTF-8)
        )
    except subprocess.CalledProcessError as exc:
        raise ValueError(
            f"Command '{command}' failed with exit code {exc.returncode}\n"
            f"Output: {exc.output}"
        ) from exc
    except OSError as exc:
        raise ValueError(f"Failed to execute command '{command}': {exc}") from exc

    return result.stdout