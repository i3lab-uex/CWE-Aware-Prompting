import shlex
import subprocess
from typing import List


def filter_and_run_command(cmd_input: str, permitted_subcommands: List[str]) -> str:
    """
    Execute a shell command only if all its tokens (the main command and
    every sub‑command) are present in the `permitted_subcommands` list.
    
    Parameters
    ----------
    cmd_input : str
        The command string supplied by the caller.
    permitted_subcommands : list[str]
        A whitelist of allowed tokens.  Every token produced by
        `shlex.split` must appear in this list; otherwise the command is rejected.
    
    Returns
    -------
    str
        The standard output produced by the executed command.
    
    Raises
    ------
    ValueError
        If `cmd_input` is empty or any token is not in the whitelist.
    RuntimeError
        If the command fails to execute (non‑zero exit status).
    """
    # Strip whitespace and guard against empty input
    cmd_input = cmd_input.strip()
    if not cmd_input:
        raise ValueError("Empty command is not allowed")

    # Split the command safely.  This preserves quoted arguments and
    # treats them as a single token.
    try:
        tokens = shlex.split(cmd_input)
    except ValueError as exc:  # e.g., unmatched quotes
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    # Ensure every token is permitted
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Command '{token}' is not allowed")

    # Execute the command safely: no shell expansion, use list of args
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False  # We'll handle non‑zero status ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {tokens[0]}") from exc

    if result.returncode != 0:
        # Return the stderr to aid debugging
        raise RuntimeError(
            f"Command failed with exit code {result.returncode}:\n{result.stderr}"
        )

    return result.stdout