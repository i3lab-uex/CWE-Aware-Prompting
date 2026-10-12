import subprocess
from typing import List


def call_system_command(sys_command: str, params: List[str]) -> str:
    """
    Execute an external command and return its standard output.

    Parameters
    ----------
    sys_command : str
        The base command to run (e.g., 'ls', 'git').
    params : list[str]
        List of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed or returns a non‑zero exit status.
    """
    # Build the full argument list for subprocess
    cmd = [sys_command] + params

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False  # We handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {sys_command}") from exc
    except OSError as exc:
        raise ValueError(f"Execution failed for {sys_command!r}: {exc}") from exc

    if result.returncode != 0:
        err_msg = result.stderr.strip() or "Unknown error"
        raise ValueError(
            f"Command '{sys_command}' failed with exit code {result.returncode}: {err_msg}"
        )

    return result.stdout.strip()