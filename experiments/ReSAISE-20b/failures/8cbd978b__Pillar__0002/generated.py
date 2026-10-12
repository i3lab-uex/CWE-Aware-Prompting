import shlex
import subprocess
from typing import List


def filter_and_run_os_command(
    exec_command: str,
    whitelisted_subcommands: List[str]
) -> str:
    """
    Execute a shell command only if all its subcommands are in the whitelist.

    Parameters
    ----------
    exec_command : str
        The command string supplied by the user.
    whitelisted_subcommands : List[str]
        A list of allowed subcommand tokens.  Each token in the
        parsed command must be present in this list.

    Returns
    -------
    str
        The combined stdout and stderr from the executed command,
        or an error message if execution is forbidden.

    Raises
    ------
    ValueError
        If the command or any subcommand is not in `whitelisted_subcommands`.
    """
    # Safely split the command into tokens
    try:
        tokens = shlex.split(exec_command)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command is not allowed.")

    # Verify every token against the whitelist
    for token in tokens:
        if token not in whitelisted_subcommands:
            raise ValueError(
                f"Forbidden subcommand detected: '{token}'. "
                "Execution aborted."
            )

    # Execute the command without invoking a shell to avoid injection
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False  # We handle non‑zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {tokens[0]}") from exc
    except Exception as exc:
        raise ValueError(f"Execution failed: {exc}") from exc

    # Combine stdout and stderr for a single string result
    output = result.stdout + result.stderr

    # Optionally, we can also return the exit code if needed
    if result.returncode != 0:
        output += f"\nCommand exited with status {result.returncode}"

    return output