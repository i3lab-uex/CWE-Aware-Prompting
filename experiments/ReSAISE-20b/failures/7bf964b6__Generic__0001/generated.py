#!/usr/bin/env python3
"""
Utility to safely validate and execute shell commands.
"""

import os
import shlex
import subprocess
from typing import List


def validate_and_execute_command(shell_cmd: str, safe_subcommands: List[str]) -> str:
    """
    Validate that all subcommands in *shell_cmd* are present in *safe_subcommands*
    and execute the command if it passes validation.

    Parameters
    ----------
    shell_cmd : str
        The complete command line to run.
    safe_subcommands : list[str]
        A whitelist of subcommands that are considered safe.

    Returns
    -------
    str
        The standard output of the executed command, or an error message if the
        command is not allowed.

    Raises
    ------
    ValueError
        If *shell_cmd* or any of its subcommands are not in the whitelist.
    """
    if not isinstance(shell_cmd, str) or not shell_cmd.strip():
        raise ValueError("Command must be a non‑empty string")

    # Split the command safely (handles quotes, escapes, etc.)
    try:
        tokens = shlex.split(shell_cmd)
    except ValueError as exc:  # e.g. unmatched quotes
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Command contains no executable part")

    # The first token is the main command; subsequent tokens are subcommands/args.
    # We only care about checking the first token and any nested subcommands
    # that might appear as arguments to other commands (e.g., `git commit`).
    # For simplicity, we validate each token that looks like a command
    # (i.e., not an option or argument starting with '-').
    for token in tokens:
        if token.startswith('-'):
            continue  # Skip options
        # If the token contains a slash, treat it as a path to an executable.
        if '/' in token:
            # Resolve the absolute path and extract the basename
            token = os.path.basename(token)
        if token not in safe_subcommands:
            raise ValueError(f"Command or subcommand '{token}' is not allowed")

    # Execute the command
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # We handle non‑zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Executable not found: {exc}") from exc
    except OSError as exc:
        raise ValueError(f"OS error during execution: {exc}") from exc

    if result.returncode != 0:
        return (
            f"Command failed with exit code {result.returncode}\n"
            f"stderr:\n{result.stderr.strip()}"
        )

    return result.stdout.strip()


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     safe = ["echo", "ls", "pwd"]
#     print(validate_and_execute_command("echo Hello, World!", safe))