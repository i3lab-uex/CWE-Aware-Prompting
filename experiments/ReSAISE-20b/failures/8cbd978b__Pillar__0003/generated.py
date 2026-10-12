import subprocess
import shlex
from typing import List

def filter_and_run_os_command(exec_command: str, whitelisted_subcommands: List[str]) -> str:
    """
    Execute a shell command only if all of its tokens are present in the
    provided whitelist.

    Parameters
    ----------
    exec_command : str
        The command string supplied by the user.
    whitelisted_subcommands : List[str]
        A list of tokens that are permitted to appear in the command.

    Returns
    -------
    str
        The standard output of the executed command, or an error message if
        execution failed.

    Raises
    ------
    ValueError
        If the command is empty or any token is not in the whitelist.
    """
    if not exec_command.strip():
        raise ValueError("No command supplied")

    # Split the command safely (no shell expansion)
    try:
        tokens = shlex.split(exec_command, posix=True)
    except ValueError as exc:
        raise ValueError(f"Malformed command: {exc}") from exc

    if not tokens:
        raise ValueError("Command contains no executable")

    # Validate each token against the whitelist
    for token in tokens:
        if token not in whitelisted_subcommands:
            raise ValueError(f"Forbidden subcommand: {token}")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False
        )
    except Exception as exc:
        return f"Execution error: {exc}"

    # Return combined stdout and stderr for visibility
    output = result.stdout.strip()
    error = result.stderr.strip()
    if error:
        return f"Error: {error}"
    return output