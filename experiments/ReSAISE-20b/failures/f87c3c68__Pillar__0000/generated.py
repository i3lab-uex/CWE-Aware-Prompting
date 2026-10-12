import shlex
import subprocess


def run_shell_command(shell_command: str, parameters: list) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    shell_command : str
        The base command to execute (e.g., "ls", "echo").
    parameters : list
        A list of string arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output of the executed command.

    Raises
    ------
    ValueError
        If the command cannot be executed, is invalid, or returns a non‑zero exit code.
    """
    if not isinstance(shell_command, str):
        raise ValueError("shell_command must be a string")

    if not isinstance(parameters, list) or not all(isinstance(p, str) for p in parameters):
        raise ValueError("parameters must be a list of strings")

    # Construct the full command list safely
    cmd = [shell_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            check=True,                # Raise CalledProcessError on non‑zero exit
            capture_output=True,
            text=True,                 # Decode bytes to str using locale encoding
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        # FileNotFoundError: command does not exist
        # CalledProcessError: non‑zero exit code
        raise ValueError(f"Command execution failed: {exc}") from exc

    return result.stdout.strip()