import os
import shlex
import subprocess
from typing import List

def restricted_command_executor(user_command: str, whitelist_commands: List[str]) -> str:
    """
    Execute a user supplied command only if all its subcommands are whitelisted.

    Parameters
    ----------
    user_command : str
        The shell command supplied by the user.
    whitelist_commands : list[str]
        A collection of permitted subcommands that may appear in the command.

    Returns
    -------
    str
        The stdout of the executed command, or an error message if execution fails.

    Raises
    ------
    ValueError
        If any token in the command is not present in ``whitelist_commands``.
    """
    # Tokenise the command safely
    tokens = shlex.split(user_command, posix=True)

    if not tokens:
        raise ValueError("No command supplied")

    # Ensure every token is allowed
    for token in tokens:
        if token not in whitelist_commands:
            raise ValueError(f"Command '{token}' is not permitted")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # we will handle non-zero exit codes ourselves
            cwd=os.getcwd()      # optional: set working directory
        )
    except FileNotFoundError:
        return f"Command not found: {tokens[0]}"
    except Exception as exc:
        return f"Execution error: {exc}"

    # Return output or error message
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Command failed with exit code {result.returncode}:\n{result.stderr.strip()}"