import shlex
import subprocess
from typing import List


def filter_and_run_os_command(exec_command: str, whitelisted_subcommands: List[str]) -> str:
    """
    Execute a shell command only if all subcommands are in the whitelist.

    Parameters
    ----------
    exec_command : str
        The command string to execute.
    whitelisted_subcommands : list[str]
        A list of allowed subcommand names.

    Returns
    -------
    str
        The standard output of the command if successful, or an error message.

    Raises
    ------
    ValueError
        If the command is empty or any subcommand is not in the whitelist.
    """
    # Strip leading/trailing whitespace and ensure we have a command
    if not exec_command or not exec_command.strip():
        raise ValueError("No command provided.")

    # Tokenise the command safely (no shell expansion)
    try:
        tokens = shlex.split(exec_command, posix=True)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Command resulted in no executable.")

    # Validate each subcommand against the whitelist
    for token in tokens:
        if token not in whitelisted_subcommands:
            raise ValueError(f"Forbidden subcommand detected: '{token}'")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False  # we handle non-zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Executable not found: {tokens[0]}") from exc
    except Exception as exc:
        raise ValueError(f"Command execution failed: {exc}") from exc

    # Build a human‑readable output
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        # Include stderr for debugging
        error_msg = result.stderr.strip() or "Unknown error"
        return f"Command failed with exit code {result.returncode}: {error_msg}"