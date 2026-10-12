import shlex
import subprocess
from typing import List


def validate_and_execute_command(
    input_command: str,
    permitted_subcommands: List[str]
) -> str:
    """
    Execute a shell command only if every token is in the list of permitted subcommands.

    Parameters
    ----------
    input_command : str
        The command string supplied by the user.
    permitted_subcommands : list[str]
        A whitelist of allowed subcommand names (tokens).  The first token
        must be the executable; all subsequent tokens are treated as arguments.

    Returns
    -------
    str
        The combined stdout and stderr from the executed command.

    Raises
    ------
    ValueError
        If the input_command is empty or if any token is not present in
        ``permitted_subcommands``.
    """
    # Strip leading/trailing whitespace and ensure the command is not empty
    trimmed = input_command.strip()
    if not trimmed:
        raise ValueError("Command is empty or only whitespace")

    # Safely split the command into tokens (no shell expansion)
    try:
        tokens = shlex.split(trimmed, posix=True)
    except ValueError as exc:  # malformed quoting etc.
        raise ValueError(f"Failed to parse command: {exc}") from exc

    # Validate each token against the whitelist
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Disallowed subcommand or argument: '{token}'")

    # Execute the command without invoking a shell (safer)
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,          # return strings instead of bytes
            check=False         # we handle non‑zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Executable not found: {exc}") from exc
    except OSError as exc:
        raise ValueError(f"OS error during execution: {exc}") from exc

    # Return stdout + stderr; callers can decide how to handle exit codes
    return result.stdout + result.stderr