import os
import shlex
import subprocess
from typing import List

def restricted_command_executor(user_command: str, whitelist_commands: List[str]) -> str:
    """
    Execute a user supplied command only if every token is in the whitelist.
    
    Parameters
    ----------
    user_command : str
        The shell command to execute.
    whitelist_commands : list[str]
        A list of allowed subcommands / arguments.

    Returns
    -------
    str
        Combined stdout and stderr from the executed command, or an error message.

    Raises
    ------
    ValueError
        If any token in the command is not present in `whitelist_commands`.
    """
    # Tokenise the user input safely (no shell expansion)
    try:
        tokens = shlex.split(user_command, posix=True)
    except ValueError as exc:          # pragma: no cover
        return f"Command parsing error: {exc}"

    if not tokens:
        raise ValueError("No command provided")

    # Verify each token against the whitelist
    for tok in tokens:
        if tok not in whitelist_commands:
            raise ValueError(f"Unauthorized token detected: {tok!r}")

    # Execute the command without invoking a shell
    try:
        completed = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,               # we handle non-zero exit codes ourselves
        )
    except FileNotFoundError as exc:  # pragma: no cover
        return f"Command not found: {exc}"
    except Exception as exc:          # pragma: no cover
        return f"Execution error: {exc}"

    output = completed.stdout + completed.stderr

    # Optionally, you can raise on non-zero exit status
    if completed.returncode != 0:
        output += f"\nCommand exited with status {completed.returncode}"

    return output