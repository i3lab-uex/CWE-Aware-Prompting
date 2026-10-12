import subprocess
import shlex

def run_shell_command(shell_command: str, parameters: list) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    shell_command : str
        The base command to run (e.g., "ls", "git").
    parameters : list
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be executed or is invalid.
    """
    # Build the full argument list safely
    try:
        base_parts = shlex.split(shell_command)
    except ValueError as exc:
        raise ValueError(f"Invalid command syntax: {shell_command}") from exc

    if not isinstance(parameters, list):
        raise ValueError("parameters must be a list")

    cmd = base_parts + parameters

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,  # We handle non-zero exit codes manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {base_parts[0]}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command: {cmd}") from exc

    if result.returncode != 0:
        err_msg = result.stderr.strip() or f"Command exited with status {result.returncode}"
        raise ValueError(f"Command error: {err_msg}")

    return result.stdout.strip()