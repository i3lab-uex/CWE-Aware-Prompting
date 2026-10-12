import shlex
import subprocess
from typing import List


def validate_and_execute_command(input_command: str, permitted_subcommands: List[str]) -> str:
    """
    Execute a shell command only if all its sub‑commands are in the list of
    permitted_subcommands.

    Parameters
    ----------
    input_command : str
        The raw command string supplied by the user.
    permitted_subcommands : list[str]
        A collection of sub‑command tokens that are allowed to appear in the
        command.  The comparison is case sensitive and performed on the token
        level (i.e., after ``shlex.split``).

    Returns
    -------
    str
        The decoded stdout of the executed command if successful, or a
        descriptive error message.

    Raises
    ------
    ValueError
        If any token in the parsed command is not found in
        ``permitted_subcommands``.
    """
    # Split the command safely into tokens (handles quotes, escapes, etc.)
    try:
        tokens = shlex.split(input_command)
    except ValueError as exc:
        # Raised if the command string is malformed (e.g. unbalanced quotes)
        raise ValueError(f"Malformed command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command is not allowed")

    # Validate each token against the permitted list
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Forbidden sub‑command detected: '{token}'")

    # Execute the command safely
    try:
        result = subprocess.run(
            tokens,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,  # returns string directly
        )
    except subprocess.CalledProcessError as exc:
        # Command executed but returned non‑zero exit status
        return f"Command failed with exit code {exc.returncode}:\n{exc.output}"
    except FileNotFoundError as exc:
        # The executable itself is missing
        return f"Executable not found: {exc}"
    except Exception as exc:
        # Catch-all for any other unforeseen errors
        return f"An unexpected error occurred: {exc}"

    # Return the command output (stdout + stderr captured)
    return result.stdout