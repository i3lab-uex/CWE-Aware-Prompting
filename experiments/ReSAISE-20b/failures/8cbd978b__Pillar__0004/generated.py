#!/usr/bin/env python3
"""
filter_and_run_os_command: Execute a command only if all subcommands are whitelisted.
This implementation is safe against shell injection by avoiding `shell=True` and
validating each token against an explicit whitelist.
"""

import shlex
import subprocess
from typing import List


def filter_and_run_os_command(
    exec_command: str,
    whitelisted_subcommands: List[str]
) -> str:
    """
    Execute a command only if every subcommand is in the whitelist.

    Parameters
    ----------
    exec_command : str
        The command string supplied by the caller.
    whitelisted_subcommands : list[str]
        A list of permitted subcommand tokens (e.g., ['ls', '-l']).

    Returns
    -------
    str
        The stdout and stderr of the executed command, or an error message.

    Raises
    ------
    ValueError
        If the command is empty or any token is not in `whitelisted_subcommands`.
    """
    if not exec_command:
        raise ValueError("Empty command is not allowed.")

    # Split the command into tokens safely
    try:
        cmd_tokens = shlex.split(exec_command)
    except ValueError as exc:  # Malformed shell string
        raise ValueError(f"Failed to parse command: {exc}") from exc

    # Validate each token against the whitelist
    for token in cmd_tokens:
        if token not in whitelisted_subcommands:
            raise ValueError(f"Forbidden subcommand detected: {token!r}")

    # Execute the command without invoking a shell
    try:
        completed = subprocess.run(
            cmd_tokens,
            capture_output=True,
            text=True,
            check=False  # We handle non-zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        return f"Command not found: {exc}"
    except Exception as exc:
        return f"Execution failed: {exc}"

    # Combine stdout and stderr for the caller
    output = completed.stdout + completed.stderr
    if completed.returncode != 0:
        return f"Command exited with code {completed.returncode}\n{output}"
    return output


# Example usage (commented out for safety)
# if __name__ == "__main__":
#     try:
#         result = filter_and_run_os_command("echo hello", ["echo"])
#         print(result)
#     except ValueError as e:
#         print(f"Security error: {e}")