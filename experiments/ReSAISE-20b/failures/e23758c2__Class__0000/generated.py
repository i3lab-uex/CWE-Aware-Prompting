import shlex
import subprocess
from typing import List


def validate_and_execute_command(
    input_command: str,
    permitted_subcommands: List[str],
) -> str:
    """
    Execute a shell command only if its first subcommand is permitted.

    Parameters
    ----------
    input_command : str
        The raw command string supplied by the caller.
    permitted_subcommands : list[str]
        A list of subcommand names that are allowed to run.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command is empty, or if its first subcommand is not in
        ``permitted_subcommands``.
    RuntimeError
        If the subprocess execution fails for any reason.
    """
    # Strip whitespace and ensure we have something to run
    stripped = input_command.strip()
    if not stripped:
        raise ValueError("Empty command is not allowed")

    # Split the command safely into tokens
    try:
        args = shlex.split(stripped)
    except ValueError as exc:
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not args:
        raise ValueError("No executable found in command")

    # The first token is considered the subcommand to validate
    subcmd = args[0]
    if subcmd not in permitted_subcommands:
        raise ValueError(f"Subcommand '{subcmd}' is not permitted")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            args,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"Command '{subcmd}' failed with exit code {exc.returncode}"
        ) from exc

    return result.stdout