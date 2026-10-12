import os
import shlex
import subprocess
from typing import List

def validate_and_execute_command(shell_cmd: str, safe_subcommands: List[str]) -> str:
    """
    Execute a shell command only if every token in the command is present
    in the list of permitted subcommands.

    Parameters
    ----------
    shell_cmd : str
        The command to run.
    safe_subcommands : list[str]
        List of tokens that are allowed. The function checks each token
        produced by ``shlex.split`` against this list.

    Returns
    -------
    str
        The standard output of the executed command if it passes validation.
        If execution fails, the exception message is returned.

    Raises
    ------
    ValueError
        If any token in the command is not found in ``safe_subcommands``.
    """
    # Parse the command safely into tokens
    try:
        cmd_tokens = shlex.split(shell_cmd)
    except ValueError as exc:
        raise ValueError(f"Invalid shell command syntax: {exc}") from None

    if not cmd_tokens:
        raise ValueError("Empty command provided")

    # Validate each token
    for token in cmd_tokens:
        if token not in safe_subcommands:
            raise ValueError(f"Disallowed subcommand or argument: '{token}'")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            cmd_tokens,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=os.environ.copy(),
        )
    except subprocess.CalledProcessError as exc:
        return f"Command failed with exit code {exc.returncode}:\n{exc.output}"
    except Exception as exc:
        return f"Unexpected error during command execution: {exc}"

    return result.stdout