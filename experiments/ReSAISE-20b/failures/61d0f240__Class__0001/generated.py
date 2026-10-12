import os
import shlex
import subprocess
from typing import List

def execute_permitted_command(input_command: str, approved_commands: List[str]) -> str:
    """
    Execute a shell command only if all tokens are in the approved list.

    Parameters
    ----------
    input_command : str
        The command string supplied by the user.
    approved_commands : list[str]
        A list of allowed subcommands (case-sensitive).

    Returns
    -------
    str
        The stdout output from the command, or an error message if execution fails.

    Raises
    ------
    ValueError
        If any token in the command is not present in ``approved_commands``.
    """
    # Tokenize input safely
    try:
        tokens = shlex.split(input_command, posix=True)
    except ValueError as exc:  # malformed command string
        return f"Command parsing error: {exc}"

    if not tokens:
        raise ValueError("Empty command is not allowed.")

    # Verify each token against the approved list
    for token in tokens:
        if token not in approved_commands:
            raise ValueError(f"Disallowed command or argument: {token!r}")

    # Execute the command with shell disabled to avoid shell injection
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # We handle non-zero exit codes ourselves
        )
    except FileNotFoundError:
        return f"Command not found: {tokens[0]}"
    except Exception as exc:
        return f"Execution failed: {exc}"

    # Return stdout or stderr based on exit status
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Error ({result.returncode}): {result.stderr.strip()}"