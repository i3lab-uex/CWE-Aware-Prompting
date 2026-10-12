import os
import shlex
import subprocess
from typing import List


def validate_and_execute_command(
    input_command: str, permitted_subcommands: List[str]
) -> str:
    """
    Execute a shell command only if every subcommand is in the permitted list.

    Parameters
    ----------
    input_command : str
        The full command string supplied by the user.
    permitted_subcommands : list[str]
        A collection of subcommand names that are allowed to run.

    Returns
    -------
    str
        The standard output of the executed command.

    Raises
    ------
    ValueError
        If any token in `input_command` is not found in `permitted_subcommands`.
    """
    # Break the command into a list of tokens safely
    try:
        cmd_tokens = shlex.split(input_command)
    except ValueError as exc:
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not cmd_tokens:
        raise ValueError("Empty command")

    # Validate every token against the permitted list
    for token in cmd_tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Disallowed subcommand: '{token}'")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            cmd_tokens,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        # Return the command output even if it failed
        return exc.output

    return result.stdout