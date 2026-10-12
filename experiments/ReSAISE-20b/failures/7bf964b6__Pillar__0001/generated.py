import os
import shlex
import subprocess
from typing import List

def validate_and_execute_command(shell_cmd: str, safe_subcommands: List[str]) -> str:
    """
    Execute a shell command only if all sub‑commands are in the list of allowed ones.

    Parameters
    ----------
    shell_cmd : str
        The command to be executed.
    safe_subcommands : list[str]
        A list of sub‑command tokens that are considered safe.

    Returns
    -------
    str
        The standard output of the executed command if it succeeds, otherwise an error message.

    Raises
    ------
    ValueError
        If the command contains any sub‑command that is not in ``safe_subcommands``.
    """
    # Split the command safely (no shell evaluation)
    try:
        tokens = shlex.split(shell_cmd, posix=True)
    except ValueError as exc:   # e.g. unmatched quotes
        raise ValueError(f"Malformed command string: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command")

    # Validate each token except the executable itself
    for idx, token in enumerate(tokens[1:], start=2):
        if token not in safe_subcommands:
            raise ValueError(
                f"Sub‑command '{token}' at position {idx} is not allowed."
            )

    # Execute the command safely (no shell=True)
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # we handle non‑zero exit codes manually
        )
    except FileNotFoundError as exc:
        return f"Executable not found: {exc}"
    except Exception as exc:
        return f"Execution error: {exc}"

    # If the command failed, provide stderr as the message
    if result.returncode != 0:
        return f"Command failed (exit {result.returncode}):\n{result.stderr.strip()}"

    return result.stdout.strip()