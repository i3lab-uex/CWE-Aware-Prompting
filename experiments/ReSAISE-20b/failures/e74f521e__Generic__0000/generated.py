import subprocess
from typing import List


def run_shell_cmd(cmd: str, params: List[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    cmd : str
        The base command to execute (e.g., 'ls', 'python').
    params : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output (and optionally error) produced by the command.

    Raises
    ------
    ValueError
        If `cmd` is empty, if any argument in `params` is not a string,
        or if the command exits with a non‑zero status.
    """
    # Basic validation
    if not isinstance(cmd, str) or not cmd.strip():
        raise ValueError("Command must be a non-empty string")

    if not isinstance(params, list):
        raise ValueError("Params must be a list of strings")

    for arg in params:
        if not isinstance(arg, str):
            raise ValueError(f"All parameters must be strings. Invalid value: {arg!r}")

    # Construct the argument list for subprocess
    full_cmd = [cmd] + params

    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            check=False  # We'll handle non‑zero exit manually
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {cmd}") from e
    except Exception as e:
        raise ValueError(f"Failed to execute command '{cmd}': {e}") from e

    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd}' failed with exit code {result.returncode}.\n"
            f"Stderr: {result.stderr.strip()}"
        )

    # Return stdout; include stderr only if it exists
    output = result.stdout.strip()
    if result.stderr:
        output += "\n" + result.stderr.strip()

    return output