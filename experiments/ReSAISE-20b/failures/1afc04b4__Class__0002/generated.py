import shlex
import subprocess
from typing import List

def run_shell_command_with_filters(command: str, allowed_subcommands_list: List[str]) -> str:
    """
    Execute a shell command after validating that the primary subcommand
    is in the allowed list and that no dangerous shell operators are used.

    Parameters:
        command (str): The full command string to execute.
        allowed_subcommands_list (List[str]): Subcommands that are permitted.

    Returns:
        str: Standard output of the command if successful, otherwise an error message.

    Raises:
        ValueError: If the command is empty, contains disallowed subcommands,
                    or includes shell operators that could lead to injection.
    """
    if not command.strip():
        raise ValueError("Command is empty")

    # Split the command into a list of arguments safely
    try:
        args = shlex.split(command, posix=True)
    except ValueError as e:  # malformed quoting
        raise ValueError(f"Invalid command syntax: {e}") from e

    if not args:
        raise ValueError("Command resolves to no executable")

    # The first token is the subcommand/executable
    subcmd = args[0]

    if subcmd not in allowed_subcommands_list:
        raise ValueError(f"Disallowed subcommand: {subcmd}")

    # Disallow common shell operators that could enable injection
    disallowed_tokens = {'|', '||', '&', '&&', ';', '>', '<', '>>', '<<'}
    for token in args[1:]:
        if token in disallowed_tokens:
            raise ValueError(f"Disallowed operator detected: {token}")

    # Execute the command safely without invoking a shell
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False,          # we'll handle non-zero exit codes manually
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {subcmd}") from e
    except Exception as e:
        raise ValueError(f"Execution failed: {e}") from e

    if result.returncode != 0:
        return f"Error: {result.stderr.strip() or 'Unknown error'}"

    return result.stdout.strip()