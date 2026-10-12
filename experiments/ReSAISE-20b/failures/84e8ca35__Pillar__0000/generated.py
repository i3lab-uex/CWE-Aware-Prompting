import os
import shlex
import subprocess
from typing import List

def restricted_command_executor(user_command: str, whitelist_commands: List[str]) -> str:
    """
    Execute a user supplied command only if all of its components are present
    in the whitelist_commands list.

    Parameters
    ----------
    user_command : str
        The raw command string supplied by the user.
    whitelist_commands : List[str]
        A list of allowed subcommands / arguments.  Every token extracted
        from the command must appear in this list.

    Returns
    -------
    str
        The combined stdout and stderr of the executed command.

    Raises
    ------
    ValueError
        If any token in the parsed command is not in whitelist_commands.
    """
    # Tokenize the command using shlex to respect quoting and escaping
    try:
        tokens = shlex.split(user_command)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command is not allowed")

    # Verify each token against the whitelist
    for tok in tokens:
        if tok not in whitelist_commands:
            raise ValueError(f"Token '{tok}' is not whitelisted")

    # Execute the command securely with shell=False
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # We handle non‑zero exit codes ourselves
            cwd=os.getcwd(),
        )
    except FileNotFoundError as exc:
        return f"Command not found: {exc}"
    except PermissionError as exc:
        return f"Permission denied: {exc}"
    except Exception as exc:     # pragma: no cover
        return f"Unexpected error during execution: {exc}"

    output = result.stdout + result.stderr
    if result.returncode != 0:
        output += f"\nCommand exited with status {result.returncode}"
    return output