import os
import shlex
import subprocess
from typing import List


def validate_and_execute_command(
    input_command: str,
    permitted_subcommands: List[str]
) -> str:
    """
    Execute a shell command only if every token in the command
    is present in ``permitted_subcommands``.
    
    Parameters
    ----------
    input_command : str
        The command string supplied by the user.
    permitted_subcommands : List[str]
        A list of tokens that are allowed to appear in the command.
    
    Returns
    -------
    str
        The combined stdout and stderr from the executed command,
        or an error message if execution is forbidden.
    
    Raises
    ------
    ValueError
        If any token in the parsed command is not present in
        ``permitted_subcommands``.
    """
    # Split the command safely into tokens
    try:
        tokens = shlex.split(input_command, posix=True)
    except ValueError as exc:  # malformed command
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command is not allowed")

    # Validate each token against the permitted list
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(
                f"Forbidden subcommand or argument: '{token}'. "
                "Only the following are allowed: "
                f"{', '.join(permitted_subcommands)}"
            )

    # Execute the command securely without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,   # We'll handle non-zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {tokens[0]}") from exc
    except Exception as exc:
        raise ValueError(f"Execution failed: {exc}") from exc

    # Combine stdout and stderr for a single string return value
    output = result.stdout + result.stderr

    # If the command failed (non-zero exit status), append a notice
    if result.returncode != 0:
        output += f"\nCommand exited with status {result.returncode}"

    return output