import os
import shlex
import subprocess
from typing import List


def restricted_command_executor(user_command: str, whitelist_commands: List[str]) -> str:
    """
    Execute a shell command only if all tokens are in the whitelist.

    Parameters
    ----------
    user_command : str
        The raw command string supplied by the user.
    whitelist_commands : list[str]
        A list of allowed subcommands. Every token in the command
        must be present in this list.

    Returns
    -------
    str
        The stdout of the executed command or an error message if the
        command could not be run.

    Raises
    ------
    ValueError
        If any token in the command is not found in ``whitelist_commands``.
    """
    # Tokenise the command safely
    try:
        tokens = shlex.split(user_command)
    except ValueError as exc:   # malformed quoting
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command is not allowed")

    # Ensure every token is whitelisted
    for tok in tokens:
        if tok not in whitelist_commands:
            raise ValueError(f"Command component '{tok}' is not permitted")

    # Execute without a shell to avoid injection
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # we handle non-zero exit ourselves
        )
    except FileNotFoundError as exc:
        return f"Command not found: {exc}"
    except PermissionError as exc:
        return f"Permission denied: {exc}"
    except Exception as exc:
        return f"Execution error: {exc}"

    # Return output or error message
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        # Include stderr for debugging
        error_msg = f"Command exited with {result.returncode}\n"
        error_msg += result.stderr.strip()
        return error_msg