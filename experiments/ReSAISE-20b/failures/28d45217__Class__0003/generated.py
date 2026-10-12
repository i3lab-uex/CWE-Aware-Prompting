import shlex
import subprocess
from typing import List

def validate_and_execute_command(input_command: str, permitted_subcommands: List[str]) -> str:
    """
    Execute a shell command only if all tokens are in the permitted_subcommands list.

    Parameters
    ----------
    input_command : str
        The command string supplied by the user.
    permitted_subcommands : list[str]
        A list of allowed subcommand tokens. Every token in the parsed command
        must appear in this list.

    Returns
    -------
    str
        The stdout of the command if it succeeds, otherwise stderr or a
        descriptive error message.

    Raises
    ------
    ValueError
        If any token in the command is not present in permitted_subcommands.
    """
    # Safely split the command into tokens
    try:
        tokens = shlex.split(input_command)
    except ValueError as exc:          # pragma: no cover
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("No command provided")

    # Validate each token against the permitted list
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Forbidden subcommand: {token}")

    # Execute the command without invoking a shell to avoid injection
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # We handle errors ourselves
        )
    except FileNotFoundError as exc:      # pragma: no cover
        return f"Command not found: {tokens[0]}"

    # Return stdout if the command succeeded, otherwise stderr
    return result.stdout.strip() or result.stderr.strip()