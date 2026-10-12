import subprocess
from typing import List

def execute_command(base_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    base_command : str
        The main command to run (e.g., "ls", "git").
    parameters : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The combined stdout and stderr output of the executed command.

    Raises
    ------
    ValueError
        If the command is empty, not a string, or the execution fails.
    """
    # Basic validation
    if not isinstance(base_command, str) or not base_command.strip():
        raise ValueError("`base_command` must be a non‑empty string.")
    if not isinstance(parameters, list):
        raise ValueError("`parameters` must be a list of strings.")
    for p in parameters:
        if not isinstance(p, str):
            raise ValueError("All elements of `parameters` must be strings.")

    # Build the command list
    cmd = [base_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,  # we handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {base_command}") from exc
    except OSError as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    # If the process exited with a non‑zero code, treat it as an error
    if result.returncode != 0:
        err_msg = (
            f"Command '{base_command}' failed with exit code {result.returncode}\n"
            f"stderr: {result.stderr.strip()}"
        )
        raise ValueError(err_msg)

    # Return the captured output (stdout + stderr)
    return result.stdout.strip()