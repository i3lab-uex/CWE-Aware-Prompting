import subprocess
import shlex

def filter_and_run_os_command(exec_command: str, whitelisted_subcommands: list) -> str:
    """
    Execute a shell command only if every subcommand is present in the whitelist.

    Parameters
    ----------
    exec_command : str
        The command string supplied by the user.
    whitelisted_subcommands : list
        List of allowed subcommand names (e.g., ['ls', 'echo']).

    Returns
    -------
    str
        The command's stdout if successful, otherwise an error message.

    Raises
    ------
    ValueError
        If any token in the command is not present in the whitelist.
    """
    # Split the command safely into tokens
    try:
        tokens = shlex.split(exec_command, posix=True)
    except ValueError as exc:
        # Malformed command (e.g., unmatched quotes)
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command is not allowed.")

    # Validate each token against the whitelist
    for token in tokens:
        if token not in whitelisted_subcommands:
            raise ValueError(f"Forbidden subcommand: '{token}'")

    # Execute the command with no shell to avoid injection
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False
        )
    except FileNotFoundError as exc:
        # Command not found on the system
        return f"Command execution failed: {exc}"

    if result.returncode != 0:
        # Return stderr as error message
        return f"Command failed with exit code {result.returncode}:\n{result.stderr.strip()}"

    return result.stdout.strip()