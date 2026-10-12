import subprocess
from typing import List


def execute_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    cmd : str
        The executable or command to run.
    arguments : list[str]
        A list of string arguments passed to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If `cmd` is empty or if the command fails to execute.
    """
    if not isinstance(cmd, str) or not cmd.strip():
        raise ValueError("Command must be a non-empty string")

    if not isinstance(arguments, list):
        raise ValueError("Arguments must be provided as a list")

    # Build the command line safely without using shell=True
    cmd_list = [cmd] + arguments

    try:
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            check=False,          # We'll handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command '{cmd}': {exc}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd}' failed with exit code {result.returncode}\n"
            f"stderr: {result.stderr.strip()}"
        )

    return result.stdout