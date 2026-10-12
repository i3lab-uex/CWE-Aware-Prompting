import subprocess
from pathlib import Path
from typing import List


def execute_shell_command(command: str, args: List[str]) -> str:
    """
    Execute a shell command with the supplied arguments and return its output.

    Parameters
    ----------
    command : str
        The base command to execute (e.g., 'ls', 'git').
    args : list
        A list of arguments for the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command is not found, if any argument is invalid,
        or if the execution fails for any reason.
    """
    # Ensure command exists on the system
    cmd_path = Path(command)
    if not cmd_path.is_file() and not shutil.which(command):
        raise ValueError(f"Command '{command}' not found on this system")

    # Build the full argument list for subprocess
    cmd_list = [command] + args

    try:
        result = subprocess.run(
            cmd_list,
            check=True,          # Raise CalledProcessError on non-zero exit
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,           # Return strings instead of bytes
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Failed to execute command '{command}': {exc}") from exc
    except subprocess.CalledProcessError as exc:
        # Include the command output in the error message
        raise ValueError(
            f"Command '{command}' failed with exit code {exc.returncode}.\n"
            f"Output:\n{exc.output}"
        ) from exc
    except Exception as exc:  # Catch-all for unforeseen errors
        raise ValueError(f"An error occurred while executing '{command}': {exc}") from exc

    return result.stdout