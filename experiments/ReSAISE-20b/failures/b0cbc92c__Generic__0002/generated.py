import subprocess
from shlex import quote

def run_command(cmd: str, cmd_arguments: list) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    cmd : str
        The base command to run.
    cmd_arguments : list
        A list of arguments (strings) to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed or returns a non‑zero exit status.
    """
    if not isinstance(cmd, str):
        raise ValueError("Command must be a string.")
    if not isinstance(cmd_arguments, list) or not all(isinstance(a, str) for a in cmd_arguments):
        raise ValueError("Arguments must be a list of strings.")

    # Construct the command safely
    cmd_list = [cmd] + cmd_arguments

    try:
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            check=True
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {cmd}") from e
    except subprocess.CalledProcessError as e:
        # Include both stdout and stderr for debugging purposes
        err_msg = f"Command '{cmd}' failed with exit code {e.returncode}.\n"
        err_msg += f"Stdout: {e.stdout}\nStderr: {e.stderr}"
        raise ValueError(err_msg) from e
    except Exception as e:
        # Catch any other unexpected exceptions
        raise ValueError(f"An error occurred while running '{cmd}': {e}") from e

    return result.stdout