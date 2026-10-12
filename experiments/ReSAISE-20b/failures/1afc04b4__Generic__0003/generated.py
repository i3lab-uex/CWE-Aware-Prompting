import shlex
import subprocess
from typing import List

def run_shell_command_with_filters(
    command: str,
    allowed_subcommands_list: List[str]
) -> str:
    """
    Execute a shell command only if its first subcommand is in the allowed list.

    Parameters
    ----------
    command : str
        The full shell command to execute.
    allowed_subcommands_list : List[str]
        A list of permitted subcommand names (e.g., ['ls', 'cat']).

    Returns
    -------
    str
        The standard output of the command if it succeeds, or an error message.

    Raises
    ------
    ValueError
        If the command is empty, cannot be parsed, or contains a disallowed subcommand.
    """
    # Strip leading/trailing whitespace and check for emptiness
    command = command.strip()
    if not command:
        raise ValueError("Empty command is not allowed.")

    # Safely split the command into tokens (no shell expansion)
    try:
        args = shlex.split(command, posix=True)
    except ValueError as exc:  # e.g., unmatched quotes
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not args:
        raise ValueError("Command parsing resulted in no tokens.")

    # The first token is the subcommand (executable)
    subcommand = args[0]
    if subcommand not in allowed_subcommands_list:
        raise ValueError(f"Disallowed subcommand: '{subcommand}'. Allowed list: {allowed_subcommands_list}")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False  # We handle non-zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        # Executable not found on the system
        raise ValueError(f"Executable '{subcommand}' not found: {exc}") from exc
    except Exception as exc:
        # Any other unexpected exception
        raise ValueError(f"Failed to execute command: {exc}") from exc

    # Return stdout on success; otherwise return stderr
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        error_msg = (
            f"Command '{command}' exited with code {result.returncode}.\n"
            f"stderr:\n{result.stderr.strip()}"
        )
        return error_msg