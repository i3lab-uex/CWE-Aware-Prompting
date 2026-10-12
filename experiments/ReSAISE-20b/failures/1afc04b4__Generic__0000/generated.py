import shlex
import subprocess
from typing import List


def run_shell_command_with_filters(
    command: str, allowed_subcommands_list: List[str]
) -> str:
    """
    Execute a shell command only if its primary subcommand is in the allowed list.

    Parameters
    ----------
    command : str
        The shell command to run.
    allowed_subcommands_list : list[str]
        List of allowed subcommand names (e.g., ["ls", "echo"]).

    Returns
    -------
    str
        The command's standard output if it executed successfully.
        If the command fails, returns a string containing the error message.

    Raises
    ------
    ValueError
        If `command` is empty, cannot be parsed, or its primary subcommand is not allowed.
    """
    if not command.strip():
        raise ValueError("Command string is empty")

    # Safely split the command into arguments
    try:
        args = shlex.split(command, posix=True)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not args:
        raise ValueError("Command contains no subcommand")

    # The first token is the primary subcommand
    subcommand = args[0]
    if subcommand not in allowed_subcommands_list:
        raise ValueError(f"Disallowed subcommand: {subcommand!r}")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False,  # We'll handle non-zero return codes ourselves
        )
    except FileNotFoundError as exc:
        # The subcommand does not exist on the system
        raise ValueError(f"Subcommand not found: {subcommand!r}") from exc
    except Exception as exc:
        # Catch any other unexpected exception during execution
        raise ValueError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        # Return stderr as the error message
        return f"Command failed with exit code {result.returncode}:\n{result.stderr.strip()}"

    return result.stdout.strip()