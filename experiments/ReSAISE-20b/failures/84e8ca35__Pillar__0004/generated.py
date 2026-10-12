import os
import shlex
import subprocess
from typing import List

def restricted_command_executor(user_command: str, whitelist_commands: List[str]) -> str:
    """
    Execute a user-supplied shell command only if every token is present in
    the whitelist_commands list.  The function does **not** use a shell to avoid
    injection attacks and returns the combined stdout/stderr output.

    Parameters
    ----------
    user_command : str
        The command string supplied by the user.
    whitelist_commands : List[str]
        A list of allowed subcommands (tokens).  Each token in the
        user_command must match one entry exactly.

    Returns
    -------
    str
        The combined stdout and stderr output from the executed command,
        or an error message if execution fails.

    Raises
    ------
    ValueError
        If any token in the command is not present in ``whitelist_commands``.
    """
    # Tokenize the user command safely
    try:
        tokens = shlex.split(user_command)
    except ValueError as exc:  # malformed quoting, etc.
        return f"Invalid command syntax: {exc}"

    if not tokens:
        return "No command provided."

    # Verify each token against the whitelist
    for token in tokens:
        if token not in whitelist_commands:
            raise ValueError(f"Command '{token}' is not allowed.")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # we handle non-zero exit codes manually
        )
    except FileNotFoundError:
        return f"Command not found: {tokens[0]}"
    except PermissionError:
        return f"Permission denied executing: {tokens[0]}"

    # Combine stdout and stderr for the caller
    output = result.stdout + result.stderr

    if result.returncode != 0:
        return f"Command exited with code {result.returncode}:\n{output}"
    return output