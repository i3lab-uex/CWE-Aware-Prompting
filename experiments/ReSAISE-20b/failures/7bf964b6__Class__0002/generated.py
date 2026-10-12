import os
import shlex
import subprocess
import re
from typing import List

# Regular expression to catch common shell metacharacters that could lead to command injection
_METACHARS_RE = re.compile(r"[;&|`$<>*?()\\]")

def validate_and_execute_command(shell_cmd: str, safe_subcommands: List[str]) -> str:
    """
    Execute a shell command only if it passes through specific filters.
    
    Parameters
    ----------
    shell_cmd : str
        The command string to be executed.
    safe_subcommands : list[str]
        A list of subcommands that are considered safe and permitted.
    
    Returns
    -------
    str
        The output of the successful command, or an error message if the command was not allowed.
    
    Raises
    ------
    ValueError
        If the command or any of its subcommands do not match the allowed list.
    """
    if not isinstance(shell_cmd, str):
        raise ValueError("Command must be a string")
    
    # Split the command safely into arguments
    try:
        args = shlex.split(shell_cmd)
    except ValueError as exc:   # e.g. unmatched quotes
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not args:
        raise ValueError("Empty command")

    # First token must be in the list of safe subcommands
    if args[0] not in safe_subcommands:
        raise ValueError(f"Subcommand '{args[0]}' is not allowed")

    # Ensure no disallowed metacharacters appear in any token
    for arg in args:
        if _METACHARS_RE.search(arg):
            raise ValueError(f"Disallowed character in argument: {arg}")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False,          # We handle non-zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Executable not found: {exc}") from exc
    except Exception as exc:
        raise ValueError(f"Execution failed: {exc}") from exc

    if result.returncode != 0:
        return f"Command failed with exit code {result.returncode}:\n{result.stderr.strip()}"

    return result.stdout.strip()