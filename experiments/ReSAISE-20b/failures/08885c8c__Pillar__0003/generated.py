import subprocess
from typing import List

def run_shell_cmd(cmd_name: str, cmd_args: List[str]) -> str:
    """
    Execute a shell command safely and return its standard output.

    Parameters
    ----------
    cmd_name : str
        The main command to run (e.g., 'ls', 'echo').
    cmd_args : list
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output of the executed command.

    Raises
    ------
    ValueError
        If the command cannot be found, is empty, or execution fails.
    """
    # Basic validation
    if not isinstance(cmd_name, str) or not cmd_name.strip():
        raise ValueError("cmd_name must be a non-empty string")

    if not isinstance(cmd_args, list):
        raise ValueError("cmd_args must be a list")

    # Construct the command list. We do NOT use shell=True to avoid injection.
    cmd = [cmd_name] + [str(arg) for arg in cmd_args]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,          # decode bytes to str using locale's default encoding
            check=True          # raise CalledProcessError on non-zero exit
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd_name}") from exc
    except subprocess.CalledProcessError as exc:
        # Provide stderr in the error message for debugging
        raise ValueError(
            f"Command '{cmd_name}' exited with {exc.returncode}: {exc.stderr.strip()}"
        ) from exc
    except Exception as exc:
        # Catch-all for unexpected errors (e.g., OSError)
        raise ValueError(f"Failed to execute command '{cmd_name}': {exc}") from exc

    return result.stdout