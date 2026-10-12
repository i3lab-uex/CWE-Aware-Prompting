import os
import shlex
import subprocess
from typing import List


def restricted_command_executor(
    user_command: str,
    whitelist_commands: List[str],
) -> str:
    """
    Execute a user‑supplied command only if every token is present in
    the whitelist.  The function uses a safe execution path (no shell)
    and returns the combined stdout/stderr of the command.

    Parameters
    ----------
    user_command : str
        The raw shell command supplied by the user.
    whitelist_commands : List[str]
        A list of permitted subcommands (tokens).  The check is
        case‑sensitive and tokenized using shlex.split.

    Returns
    -------
    str
        Combined stdout and stderr of the executed command, or an error
        message if the command contains disallowed tokens.

    Raises
    ------
    ValueError
        If any token in the command is not present in ``whitelist_commands``.
    RuntimeError
        If the subprocess fails to start or returns a non‑zero exit status.
    """
    # Tokenise the user command safely
    try:
        tokens = shlex.split(user_command)
    except ValueError as exc:  # malformed command
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command is not allowed")

    # Ensure every token is in the whitelist
    for token in tokens:
        if token not in whitelist_commands:
            raise ValueError(f"Disallowed command or argument: '{token}'")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # we handle non‑zero exit manually
        )
    except OSError as exc:
        raise RuntimeError(f"Execution failed: {exc}") from exc

    # Combine stdout and stderr for a single string
    output = result.stdout + result.stderr

    if result.returncode != 0:
        raise RuntimeError(
            f"Command exited with status {result.returncode}:\n{output}"
        )

    return output