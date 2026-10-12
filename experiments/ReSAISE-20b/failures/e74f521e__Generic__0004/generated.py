import subprocess
import shlex
from typing import List

def run_shell_cmd(cmd: str, params: List[str]) -> str:
    """
    Execute a shell command with the given parameters and return its output.

    Parameters
    ----------
    cmd : str
        The command to run (e.g., "ls", "grep").
    params : list of str
        Arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed or returns a non‑zero exit status.
    """
    # Ensure cmd is not empty
    if not cmd:
        raise ValueError("Command must be a non‑empty string")

    # Build the argument list.  Use shlex.quote to protect any
    # elements that may contain shell metacharacters if the user later
    # decides to run with `shell=True`.  Here we use shell=False,
    # so quoting is not strictly necessary but keeps the interface
    # safe if the function evolves.
    args = [cmd] + params

    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            shell=False,          # Do not use the shell to avoid injection
            check=False           # We'll handle errors ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        # Include stderr in the error message for diagnostics
        raise ValueError(
            f"Command '{cmd}' failed with exit code {result.returncode}.\n"
            f"Stderr: {result.stderr.strip()}"
        )

    return result.stdout