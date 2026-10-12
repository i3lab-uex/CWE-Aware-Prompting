import os
import shlex
import subprocess
from typing import List

def filter_and_run_os_command(
    exec_command: str,
    whitelisted_subcommands: List[str]
) -> str:
    """
    Execute a shell command only if all of its subcommands are whitelisted.

    Parameters
    ----------
    exec_command : str
        The full command string the user wants to execute.
    whitelisted_subcommands : List[str]
        A list of subcommand tokens that are allowed.

    Returns
    -------
    str
        The command's stdout on success, or an error message if the command
        is forbidden.

    Raises
    ------
    ValueError
        If any subcommand token in the command is not present in
        `whitelisted_subcommands`.
    """
    # Safely split the command into tokens.
    try:
        tokens = shlex.split(exec_command)
    except ValueError as exc:
        # shlex can raise if the command is malformed.
        return f"Error: Malformed command – {exc}"

    # Validate each token against the whitelist.
    for token in tokens:
        if token not in whitelisted_subcommands:
            raise ValueError(
                f"Forbidden subcommand detected: '{token}'. "
                "Command not executed."
            )

    # All tokens are allowed – execute the command.
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # We handle non-zero exit codes ourselves.
        )
    except FileNotFoundError:
        return f"Error: Command not found – {tokens[0]}"
    except Exception as exc:
        return f"Error: Failed to execute command – {exc}"

    # Build a user‑friendly output.
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        # Include stderr in the error message.
        err_msg = result.stderr.strip() or "Unknown error."
        return (
            f"Command failed with exit code {result.returncode}: "
            f"{err_msg}"
        )