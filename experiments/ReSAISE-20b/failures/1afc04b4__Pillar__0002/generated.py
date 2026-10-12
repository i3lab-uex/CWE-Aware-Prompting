import subprocess
import shlex
from typing import List

def run_shell_command_with_filters(command: str,
                                   allowed_subcommands_list: List[str]) -> str:
    """
    Execute a shell command only if all sub‑commands are in the allowed list.

    Parameters
    ----------
    command : str
        The full shell command to run.
    allowed_subcommands_list : list[str]
        A list of sub‑command tokens that are permitted.

    Returns
    -------
    str
        The stdout from the command if it succeeded, or an error message.

    Raises
    ------
    ValueError
        If the command is empty or contains any token that is not in the
        allowed_subcommands_list.
    """
    if not command.strip():
        raise ValueError("Empty command is not allowed")

    # Split the command safely; shlex.split respects quoting and escapes
    tokens = shlex.split(command)

    # Validate each token against the whitelist
    for token in tokens:
        if token not in allowed_subcommands_list:
            raise ValueError(f"Disallowed subcommand or argument: {token!r}")

    # Execute the command without invoking a shell to avoid injection
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False
        )
    except OSError as exc:
        return f"Execution failed: {exc}"

    # Return stdout on success; otherwise return stderr
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Command failed (exit {result.returncode}):\n{result.stderr.strip()}"