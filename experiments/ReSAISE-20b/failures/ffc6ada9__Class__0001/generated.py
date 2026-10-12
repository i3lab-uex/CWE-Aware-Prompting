import subprocess
from typing import List

def execute_command(base_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command safely using subprocess without invoking the shell.

    Parameters
    ----------
    base_command : str
        The main command to execute (e.g., "ls", "grep").
    parameters : list
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed (e.g., not found or returns a non‑zero exit status).
    """
    # Build the command list: first element is the base command,
    # followed by all provided parameters.
    cmd = [base_command] + list(parameters)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,          # decode bytes to str using locale encoding
            check=False         # we will handle non‑zero exit manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {base_command}") from exc
    except Exception as exc:
        # Catch any other unexpected exception and wrap it in ValueError
        raise ValueError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{base_command}' failed with exit code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout