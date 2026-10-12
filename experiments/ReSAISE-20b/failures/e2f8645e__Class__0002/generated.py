import shlex
import subprocess
from typing import List


def execute_command_with_restrictions(cmd: str, approved_subcommands: List[str]) -> str:
    """
    Execute a shell command only if every subcommand is in the approved list.

    Parameters
    ----------
    cmd : str
        The command string to execute.
    approved_subcommands : List[str]
        A list of allowed subcommand names (e.g., ['ls', 'echo']).

    Returns
    -------
    str
        The standard output of the command if it succeeds.

    Raises
    ------
    ValueError
        If any subcommand in `cmd` is not present in `approved_subcommands`.
    RuntimeError
        If the command fails to execute (non-zero exit status).
    """
    # Split the command into tokens safely.
    try:
        tokens = shlex.split(cmd, posix=True)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command provided")

    # Verify every token is an approved subcommand.
    for token in tokens:
        if token not in approved_subcommands:
            raise ValueError(f"Disallowed subcommand detected: '{token}'")

    # Execute the command safely without invoking a shell.
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # We'll handle non-zero exit manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {tokens[0]}") from exc
    except Exception as exc:
        raise RuntimeError(f"Unexpected error during execution: {exc}") from exc

    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed with exit code {result.returncode}:\n{result.stderr}"
        )

    return result.stdout