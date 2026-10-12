import os
import shlex
import subprocess
from typing import List


def validate_and_execute_command(
    input_command: str,
    permitted_subcommands: List[str],
) -> str:
    """
    Execute a shell command only if every token in the command is present
    in `permitted_subcommands`.

    Parameters
    ----------
    input_command : str
        The command the user wants to execute.
    permitted_subcommands : list[str]
        A collection of allowed subcommand tokens.

    Returns
    -------
    str
        The combined stdout and stderr produced by the command.

    Raises
    ------
    ValueError
        If `input_command` is empty or any token in the command is not found
        in `permitted_subcommands`.
    """
    # Trim whitespace and ensure the command is not empty
    cleaned = input_command.strip()
    if not cleaned:
        raise ValueError("No command provided")

    # Safely split the command into tokens (handles quoting, escapes, etc.)
    try:
        tokens = shlex.split(cleaned)
    except ValueError as exc:  # malformed quoting
        raise ValueError(f"Failed to parse command: {exc}") from exc

    # Validate each token against the permitted list
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Token '{token}' is not an allowed subcommand")

    # Execute the command safely (no shell expansion)
    result = subprocess.run(
        tokens,
        capture_output=True,
        text=True,
        check=False,          # We will handle non‑zero exit codes ourselves
    )

    # Combine stdout and stderr for the caller to see everything
    output = result.stdout + result.stderr

    # Optionally raise if the command failed (non‑zero exit status)
    if result.returncode != 0:
        raise ValueError(
            f"Command exited with status {result.returncode}:\n{output}"
        )

    return output