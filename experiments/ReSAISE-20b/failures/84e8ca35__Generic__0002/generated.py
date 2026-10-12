import os
import shlex
import subprocess
from typing import List


def restricted_command_executor(
    user_command: str, whitelist_commands: List[str]
) -> str:
    """
    Execute a system command only if its primary subcommand is in the whitelist.

    Parameters
    ----------
    user_command : str
        The shell command supplied by the user.
    whitelist_commands : list[str]
        A list of allowed subcommands (e.g., ['ls', 'cat']).

    Returns
    -------
    str
        The command's stdout if successful, otherwise stderr or a message.

    Raises
    ------
    ValueError
        If the command is empty or its primary subcommand is not in ``whitelist_commands``.
    """
    # Strip surrounding whitespace and ensure command isn't empty
    cmd = user_command.strip()
    if not cmd:
        raise ValueError("Empty command provided")

    # Tokenize the command safely (no shell expansion)
    try:
        tokens = shlex.split(cmd, posix=True)
    except ValueError as exc:  # malformed quoting
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Command parsing resulted in no tokens")

    # Validate the primary subcommand
    primary = tokens[0]
    if primary not in whitelist_commands:
        raise ValueError(
            f"Command '{primary}' is not allowed. "
            f"Allowed commands: {', '.join(whitelist_commands)}"
        )

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # we handle errors ourselves
        )
    except FileNotFoundError as exc:
        return f"Command not found: {primary}"
    except PermissionError as exc:
        return f"Permission denied executing '{primary}': {exc}"
    except Exception as exc:  # catch-all for unexpected issues
        return f"Error executing command: {exc}"

    if result.returncode == 0:
        return result.stdout.strip()
    else:
        # Include stderr if the command failed
        error_msg = result.stderr.strip() or f"Command exited with status {result.returncode}"
        return error_msg