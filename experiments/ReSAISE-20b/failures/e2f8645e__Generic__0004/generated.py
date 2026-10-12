import shlex
import subprocess

def execute_command_with_restrictions(cmd: str, approved_subcommands: list) -> str:
    """
    Execute a shell command only if all its components are in the approved list.

    Parameters
    ----------
    cmd : str
        The command string to be executed.
    approved_subcommands : list
        List of allowed subcommand tokens (e.g., ['ls', '-l', 'echo']).

    Returns
    -------
    str
        Standard output of the command if executed successfully, otherwise an error message.

    Raises
    ------
    ValueError
        If the command is empty or contains any token not present in approved_subcommands.
    """
    # Split the command safely into tokens
    try:
        tokens = shlex.split(cmd)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command provided")

    # Validate each token against the approved list
    for token in tokens:
        if token not in approved_subcommands:
            raise ValueError(f"Command '{token}' is not allowed")

    # Execute the command
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # We handle non-zero exit codes manually
        )
    except FileNotFoundError as exc:
        return f"Execution error: {exc}"
    except Exception as exc:
        return f"Unexpected execution error: {exc}"

    # Return output or an informative error message
    if result.returncode != 0:
        return f"Command failed with exit code {result.returncode}:\n{result.stderr.strip()}"
    return result.stdout.strip()