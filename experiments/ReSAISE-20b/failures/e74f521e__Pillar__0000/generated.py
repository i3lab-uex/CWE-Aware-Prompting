import subprocess
from typing import List

def run_shell_cmd(cmd: str, params: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    cmd : str
        The base command to execute.
    params : list of str
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed, is invalid, or returns a non‑zero exit status.
    """
    if not isinstance(cmd, str) or not cmd:
        raise ValueError("Command must be a non‑empty string")

    if not isinstance(params, list):
        raise ValueError("Params must be a list of strings")

    # Ensure all parameters are strings
    for p in params:
        if not isinstance(p, str):
            raise ValueError("All parameters must be strings")

    # Construct the argument list
    args = [cmd] + params

    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False  # We'll handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command '{cmd}': {exc}") from exc

    if result.returncode != 0:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command '{cmd}' exited with status {result.returncode}.\n"
            f"Stderr: {result.stderr.strip()}"
        )

    return result.stdout