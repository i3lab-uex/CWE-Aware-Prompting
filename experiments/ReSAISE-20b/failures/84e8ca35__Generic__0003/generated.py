import shlex
import subprocess
from typing import List


def restricted_command_executor(user_command: str, whitelist_commands: List[str]) -> str:
    """
    Execute a user supplied shell command while ensuring that all tokens are
    present in the whitelist.

    Parameters
    ----------
    user_command : str
        The command string supplied by a user.
    whitelist_commands : list[str]
        List of tokens that are allowed to appear in the command.

    Returns
    -------
    str
        The combined stdout and stderr of the executed command, or an error
        message if the command is not allowed.

    Raises
    ------
    ValueError
        If any token in the command is not present in ``whitelist_commands``.
    """
    # Split the command safely (no shell interpretation)
    try:
        tokens = shlex.split(user_command, posix=True)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command")

    # Verify that every token is in the whitelist
    for token in tokens:
        if token not in whitelist_commands:
            raise ValueError(f"Command '{token}' is not allowed")

    # Execute the command without invoking a shell
    try:
        completed = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # We'll handle non‑zero return codes ourselves
        )
    except OSError as exc:
        return f"Execution failed: {exc}"

    # Combine stdout and stderr for the caller
    output = completed.stdout
    if completed.stderr:
        output += f"\n[stderr]\n{completed.stderr}"

    return output