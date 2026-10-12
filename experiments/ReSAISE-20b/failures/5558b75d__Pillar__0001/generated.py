import os
import shlex
import subprocess
from typing import List


def filter_and_run_command(cmd_input: str, permitted_subcommands: List[str]) -> str:
    """
    Execute a shell command only if it contains at least one permitted subcommand.

    Parameters
    ----------
    cmd_input : str
        The command string to be executed.
    permitted_subcommands : list[str]
        A list of subcommand strings considered safe. The command will be allowed
        if any token in the parsed command matches one of these.

    Returns
    -------
    str
        The standard output from the executed command, or an error message if
        execution failed.

    Raises
    ------
    ValueError
        If the command does not contain any permitted subcommand or if parsing
        fails.
    """
    # 1. Parse the command safely with shlex to avoid shell injection
    try:
        args = shlex.split(cmd_input, posix=True)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not args:
        raise ValueError("Empty command provided")

    # 2. Validate that at least one token matches a permitted subcommand
    if not any(token in permitted_subcommands for token in args):
        raise ValueError("Command or subcommand not allowed")

    # 3. Execute the command without invoking a shell
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False,  # We handle errors ourselves
        )
    except OSError as exc:
        return f"Execution failed: {exc}"

    # 4. Return stdout or stderr based on exit status
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        # Provide a clear error message while avoiding leaking sensitive data
        return f"Command failed with exit code {result.returncode}: {result.stderr.strip()}"