import shlex
import subprocess

def run_shell_command_with_filters(command: str, allowed_subcommands_list: list) -> str:
    """
    Execute a shell command only if its primary subcommand is in the allowed list.

    Parameters
    ----------
    command : str
        The shell command to run.
    allowed_subcommands_list : list
        A list of allowed subcommand names (e.g., ['ls', 'cat']).

    Returns
    -------
    str
        The standard output of the command.

    Raises
    ------
    ValueError
        If the command is empty, contains no subcommand, or uses a disallowed subcommand.
    RuntimeError
        If the subprocess fails to execute successfully.
    """
    if not command or not command.strip():
        raise ValueError("Command is empty")

    # Safely split the command into tokens
    try:
        tokens = shlex.split(command)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("No subcommand found in the command")

    primary_subcommand = tokens[0]

    if primary_subcommand not in allowed_subcommands_list:
        raise ValueError(f"Disallowed subcommand: {primary_subcommand}")

    # Execute the command without invoking a shell to avoid shell injection
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # We'll handle non-zero exit codes ourselves
        )
    except Exception as exc:
        raise RuntimeError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed with exit code {result.returncode}:\n{result.stderr.strip()}"
        )

    return result.stdout