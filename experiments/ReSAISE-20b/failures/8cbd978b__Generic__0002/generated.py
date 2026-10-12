import shlex
import subprocess
from typing import List

def filter_and_run_os_command(exec_command: str, whitelisted_subcommands: List[str]) -> str:
    """
    Execute a shell command only if every token is in the whitelist.

    Parameters
    ----------
    exec_command : str
        The command string supplied by the user.
    whitelisted_subcommands : List[str]
        A list of permitted subcommand tokens.  The comparison is exact
        (case‑sensitive).  Tokens that are not present in this list will
        cause a ValueError to be raised.

    Returns
    -------
    str
        The combined stdout and stderr of the executed command, or an
        error message if a forbidden subcommand is detected.

    Raises
    ------
    ValueError
        If any token in ``exec_command`` is not present in
        ``whitelisted_subcommands``.
    """
    # Break the command into safe tokens
    try:
        tokens = shlex.split(exec_command)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command provided")

    # Validate each token
    for token in tokens:
        if token not in whitelisted_subcommands:
            raise ValueError(f"Forbidden subcommand: '{token}'")

    # Execute the command securely
    try:
        completed = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False  # We want to return output even if non-zero exit
        )
    except OSError as exc:
        # This occurs if the executable itself is missing or not allowed
        return f"Execution failed: {exc}"

    # Combine stdout and stderr for the caller's convenience
    output = completed.stdout + completed.stderr
    return output.strip() or f"Command executed with exit code {completed.returncode}"