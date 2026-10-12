#!/usr/bin/env python3
"""
filter_and_run_command

Executes a shell command only if all of its tokens (subcommands) are present
in a supplied whitelist.  The function is safe against shell injection
because it never passes the command string to a shell; instead it uses
`shlex.split` and `subprocess.run`.

The implementation follows best practices for input validation (CWE‑707)
by ensuring the command is well‑formed and that every token matches an
allowed value before any system call is made.
"""

import shlex
import subprocess
from typing import List


def filter_and_run_command(cmd_input: str, permitted_subcommands: List[str]) -> str:
    """
    Execute a command only if every token in the parsed command is allowed.

    Parameters
    ----------
    cmd_input : str
        The raw command string supplied by the caller.
    permitted_subcommands : list[str]
        A whitelist of subcommand tokens that are considered safe.

    Returns
    -------
    str
        The standard output of the executed command, or an error message if
        execution failed.

    Raises
    ------
    ValueError
        If the command contains any token that is not in ``permitted_subcommands``.
    """
    # 1. Parse the command safely; shlex.split handles quoting and escapes.
    try:
        tokens = shlex.split(cmd_input)
    except ValueError as exc:  # malformed quoting
        raise ValueError(f"Malformed command string: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command is not allowed")

    # 2. Validate every token against the whitelist.
    for tok in tokens:
        if tok not in permitted_subcommands:
            raise ValueError(f"Command '{tok}' is not permitted")

    # 3. Execute the command without invoking a shell.
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # we handle non‑zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        # The first token (executable) does not exist
        return f"Executable not found: {exc}"
    except Exception as exc:
        # Catch-all for unexpected errors
        return f"Execution failed: {exc}"

    # 4. Return output or error message.
    if result.returncode != 0:
        return (
            f"Command exited with {result.returncode}.\n"
            f"stderr:\n{result.stderr}"
        )

    return result.stdout


# Example usage (commented out to avoid accidental execution)
# if __name__ == "__main__":
#     whitelist = ["echo", "-n", "Hello, world!"]
#     print(filter_and_run_command("echo -n Hello, world!", whitelist))