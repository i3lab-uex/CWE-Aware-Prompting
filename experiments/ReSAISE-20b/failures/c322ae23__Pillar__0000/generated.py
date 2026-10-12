import subprocess
import shlex

def run_command_with_args(base_command: str, parameters: list) -> str:
    """
    Execute an external command safely with the provided arguments.

    Parameters
    ----------
    base_command : str
        The primary command to run (e.g., "ls", "git commit").
    parameters : list
        A list of string arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output from the executed command.

    Raises
    ------
    ValueError
        If the command is invalid, fails to execute, or returns a non‑zero exit status.
    """
    # Split the base command into tokens without using a shell
    try:
        cmd_tokens = shlex.split(base_command, posix=True)
    except ValueError as exc:
        raise ValueError(f"Invalid base command: {base_command!r}") from exc

    # Ensure all parameters are strings
    if not all(isinstance(p, str) for p in parameters):
        raise ValueError("All parameters must be strings")

    # Build the full command list
    cmd = cmd_tokens + parameters

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,          # returns str instead of bytes
            check=False         # handle non‑zero exit manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd_tokens[0]!r}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command: {cmd!r}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command exited with non‑zero status {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout