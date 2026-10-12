import os
import shlex
import subprocess
from typing import List


def filter_and_run_os_command(exec_command: str, whitelisted_subcommands: List[str]) -> str:
    """
    Execute a shell command only if every subcommand token is present in the
    provided whitelist.  The function uses :mod:`shlex` to safely split the
    command string and :func:`subprocess.run` for execution.  Any token not in
    the whitelist will raise a :class:`ValueError`.

    Parameters
    ----------
    exec_command:
        The command string supplied by the caller.
    whitelisted_subcommands:
        A list of allowed tokens.  The function checks each token in the
        parsed command against this list.

    Returns
    -------
    str
        The standard output of the executed command if successful, or an error
        message explaining why execution failed.

    Raises
    ------
    ValueError
        If the command is empty or any token is not in ``whitelisted_subcommands``.
    """
    if not exec_command.strip():
        raise ValueError("Empty command is not allowed")

    # Split the command safely
    try:
        tokens = shlex.split(exec_command)
    except ValueError as exc:  # e.g., unmatched quotes
        raise ValueError(f"Failed to parse command: {exc}") from exc

    # Validate every token against the whitelist
    for token in tokens:
        if token not in whitelisted_subcommands:
            raise ValueError(
                f"Command '{token}' is not in the whitelist of allowed subcommands."
            )

    # Execute command safely; do not use shell=True to avoid shell injection
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # we handle errors ourselves
        )
    except Exception as exc:  # pragma: no cover
        return f"Execution failed: {exc}"

    if result.returncode != 0:
        # Return stderr to provide context on failure
        return f"Command failed with exit code {result.returncode}:\n{result.stderr.strip()}"
    return result.stdout.strip()