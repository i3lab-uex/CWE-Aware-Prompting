import subprocess
from typing import List

def run_command_with_args(base_command: str, parameters: List[str]) -> str:
    """
    Execute a command with the supplied arguments and return its output.

    Parameters
    ----------
    base_command : str
        The executable to run (e.g., "ls", "/usr/bin/grep").
    parameters : list[str]
        List of command‑line arguments for the executable.

    Returns
    -------
    str
        The standard output produced by the command, decoded using UTF‑8.

    Raises
    ------
    ValueError
        If the command cannot be found or execution fails.
    """
    if not isinstance(base_command, str):
        raise ValueError("base_command must be a string")
    if not isinstance(parameters, list) or not all(isinstance(p, str) for p in parameters):
        raise ValueError("parameters must be a list of strings")

    # Build the command list.  Using shell=False prevents shell
    # interpretation of arguments, mitigating CWE‑77.
    cmd = [base_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,          # automatically decodes bytes to str
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {base_command}") from e
    except subprocess.CalledProcessError as e:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command '{base_command}' failed with exit code {e.returncode}:\n"
            f"{e.stderr}"
        ) from e

    return result.stdout