import subprocess
from typing import List

def execute_command(cmd: str, arguments: List[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    cmd : str
        The base command to execute (e.g., "ls", "grep").
    arguments : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output from the executed command.

    Raises
    ------
    ValueError
        If the command cannot be executed or is invalid.
    """
    # Build a safe list of arguments for subprocess
    if not isinstance(cmd, str) or not cmd.strip():
        raise ValueError("Command must be a non-empty string")

    if not isinstance(arguments, list):
        raise ValueError("Arguments must be a list")

    # Construct the command as a list to avoid shell injection
    cmd_list = [cmd] + arguments

    try:
        # Run the command without invoking a shell for security
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,          # decode bytes to str using locale encoding
            check=True,         # raise CalledProcessError on non-zero exit
        )
    except FileNotFoundError as e:
        # The command binary was not found on the system
        raise ValueError(f"Command '{cmd}' not found") from e
    except subprocess.CalledProcessError as e:
        # Command executed but returned a non-zero exit status
        raise ValueError(
            f"Command '{cmd}' failed with return code {e.returncode}\n"
            f"Stdout: {e.stdout}\nStderr: {e.stderr}"
        ) from e
    except Exception as e:
        # Catch-all for unexpected errors
        raise ValueError(f"Failed to execute command '{cmd}': {e}") from e

    return result.stdout