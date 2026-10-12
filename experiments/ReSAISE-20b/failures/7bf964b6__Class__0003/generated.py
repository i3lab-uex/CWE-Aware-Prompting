import os
import shlex
import subprocess
from typing import List


def validate_and_execute_command(shell_cmd: str, safe_subcommands: List[str]) -> str:
    """
    Execute a shell command only if all of its subcommands are in the
    safe_subcommands list.

    Parameters
    ----------
    shell_cmd : str
        The command string to be executed.
    safe_subcommands : List[str]
        A list of subcommands (tokens) that are allowed to be used.

    Returns
    -------
    str
        The standard output of the executed command.

    Raises
    ------
    ValueError
        If any token in the command is not present in safe_subcommands.
    """
    # Split the command into tokens safely
    try:
        tokens = shlex.split(shell_cmd)
    except ValueError as exc:
        raise ValueError(f"Invalid shell command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command provided")

    # Validate each token against the allowed list
    for token in tokens:
        if token not in safe_subcommands:
            raise ValueError(
                f"Disallowed subcommand detected: '{token}'. "
                "Command execution aborted."
            )

    # Execute the command without invoking a shell to avoid injection
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=True,  # Raises CalledProcessError on non-zero exit
        )
    except subprocess.CalledProcessError as exc:
        # Return the error output for debugging
        return (
            f"Command failed with exit code {exc.returncode}:\n"
            f"{exc.stderr}"
        )
    except FileNotFoundError as exc:
        return f"Command not found: {exc}"

    # Return the captured standard output
    return result.stdout.strip()