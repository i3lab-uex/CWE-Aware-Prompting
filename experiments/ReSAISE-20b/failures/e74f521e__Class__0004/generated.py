import subprocess
from typing import List

def run_shell_cmd(cmd: str, params: List[str]) -> str:
    """
    Execute a shell command safely and return its output.

    Parameters
    ----------
    cmd : str
        The executable to run (e.g., "ls", "/usr/bin/grep").
    params : list
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The stdout produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed, if it returns a non‑zero exit status,
        or if the executable is not found.
    """
    # Build the command list.  Do *not* use shell=True to avoid
    # CWE‑77 (command injection).  Each element is passed verbatim.
    command = [cmd] + params

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False  # We'll handle non‑zero return ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command '{cmd}': {exc}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd}' exited with status {result.returncode}:\n{result.stderr}"
        )

    return result.stdout