import subprocess
from typing import List

def call_system_command(sys_command: str, params: List[str]) -> str:
    """
    Execute an external command with the supplied arguments and return its output.

    Args:
        sys_command (str): The primary command to run. Must be a valid executable name.
        params (List[str]): A list of arguments for the command.

    Returns:
        str: The standard output produced by the executed command.

    Raises:
        ValueError: If the command is missing, not executable, or fails during execution.
    """
    if not isinstance(sys_command, str) or not sys_command.strip():
        raise ValueError("`sys_command` must be a non-empty string")

    if not isinstance(params, list) or any(
        not isinstance(p, str) for p in params
    ):
        raise ValueError("`params` must be a list of strings")

    # Build the command as a list to avoid shell injection.
    cmd = [sys_command] + params

    try:
        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,   # decode bytes to str using locale encoding
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {sys_command}") from exc
    except subprocess.CalledProcessError as exc:
        raise ValueError(
            f"Command '{sys_command}' failed with exit code {exc.returncode}: "
            f"{exc.output}"
        ) from exc

    return result.stdout