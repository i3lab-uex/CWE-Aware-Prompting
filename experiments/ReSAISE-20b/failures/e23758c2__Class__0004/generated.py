import shlex
import subprocess
from typing import List

def validate_and_execute_command(
    input_command: str,
    permitted_subcommands: List[str]
) -> str:
    """
    Execute a shell command only if all sub‑commands are in the
    permitted_subcommands list.

    Parameters
    ----------
    input_command : str
        The command string supplied by the user.
    permitted_subcommands : list[str]
        A list of tokens that are allowed to appear in the command.

    Returns
    -------
    str
        The stdout of the executed command (decoded as UTF‑8).

    Raises
    ------
    ValueError
        If any token in the command is not present in `permitted_subcommands`.
    """
    # Safely split the input into tokens; this handles quotes, escapes, etc.
    try:
        tokens = shlex.split(input_command)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("No command provided")

    # Validate each token against the allowed list
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Token '{token}' is not allowed")

    # Execute the command without invoking a shell to avoid injection.
    try:
        result = subprocess.run(
            tokens,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,          # equivalent to encoding='utf-8'
        )
    except subprocess.CalledProcessError as exc:
        # Return the command's output even if it failed
        return exc.stdout

    return result.stdout