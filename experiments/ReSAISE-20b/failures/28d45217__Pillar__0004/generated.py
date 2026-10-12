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
    permitted_subcommands : List[str]
        A collection of subcommands that are allowed to be executed.

    Returns
    -------
    str
        The command's standard output if execution succeeds, otherwise an error message.

    Raises
    ------
    ValueError
        If the command or any of its tokens is not found in ``permitted_subcommands``.
    """
    # Tokenise the command safely
    try:
        tokens = shlex.split(input_command)
    except ValueError as exc:  # e.g. unmatched quotes
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command provided")

    # Validate each token against the permitted list
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Forbidden subcommand: '{token}'")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False
        )
    except FileNotFoundError as exc:
        return f"Command not found: {tokens[0]}"
    except Exception as exc:
        # Catch-all for unexpected runtime errors
        return f"Execution failed: {exc}"

    if result.returncode != 0:
        # Include stderr in the error message for clarity
        return f"Command failed with exit code {result.returncode}:\n{result.stderr.strip()}"

    return result.stdout.strip()