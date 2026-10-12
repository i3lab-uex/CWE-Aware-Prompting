import os
import shlex
import subprocess
from typing import List

def filter_and_run_command(cmd_input: str, permitted_subcommands: List[str]) -> str:
    """
    Execute a shell command only if all its sub‑commands are in the permitted list.

    Parameters
    ----------
    cmd_input : str
        The command string to be executed.
    permitted_subcommands : list[str]
        A list of sub‑command names that are considered safe.

    Returns
    -------
    str
        The standard output of the command if it executed successfully, or an error message.

    Raises
    ------
    ValueError
        If the command is empty or any sub‑command is not in the permitted list.
    """
    # Strip whitespace and ensure command is not empty
    cmd_input = cmd_input.strip()
    if not cmd_input:
        raise ValueError("No command provided.")

    # Parse the command safely
    try:
        tokens = shlex.split(cmd_input)
    except ValueError as exc:  # malformed command string
        raise ValueError(f"Failed to parse command: {exc}") from exc

    # Validate every sub‑command against the allowed list
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(
                f"Sub‑command '{token}' is not allowed. "
                f"Permitted sub‑commands: {', '.join(permitted_subcommands)}"
            )

    # Execute the command
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # we handle errors manually
        )
    except OSError as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    # Return output or error message
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        # Include stderr in the error message for debugging
        error_msg = result.stderr.strip() or "Unknown error"
        return f"Command failed with exit code {result.returncode}: {error_msg}"