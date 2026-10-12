import shlex
import subprocess
from typing import List


def validate_and_execute_command(
    input_command: str,
    permitted_subcommands: List[str],
) -> str:
    """
    Execute a shell command only if every token (subcommand and arguments)
    is present in the list of permitted subcommands.

    Parameters
    ----------
    input_command : str
        The full command string supplied by the user.
    permitted_subcommands : list[str]
        A list of allowed tokens.  Every token in the parsed command
        must be present in this list.

    Returns
    -------
    str
        The standard output of the executed command, decoded as UTF‑8.

    Raises
    ------
    ValueError
        If the command is empty, contains a token not in `permitted_subcommands`,
        or if execution fails.
    """
    # Strip whitespace and ensure something was provided
    stripped = input_command.strip()
    if not stripped:
        raise ValueError("No command supplied")

    # Safely split the command into tokens
    try:
        tokens = shlex.split(stripped)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    # Validate every token against the permitted list
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Token '{token}' is not allowed")

    # Execute the command without invoking a shell to avoid injection
    try:
        completed = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=True,          # raise CalledProcessError on non‑zero exit
        )
    except subprocess.CalledProcessError as exc:
        # Provide the stderr in the exception message for debugging
        raise ValueError(
            f"Command execution failed (exit {exc.returncode}): "
            f"{exc.stderr.strip()}"
        ) from exc
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {tokens[0]}") from exc

    return completed.stdout