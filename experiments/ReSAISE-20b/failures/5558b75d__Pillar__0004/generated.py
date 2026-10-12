#!/usr/bin/env python3
"""
filter_and_run_command.py

A safe wrapper that executes a shell command only if it matches an
explicitly permitted list of subcommands.  The function uses the
`shlex` module to parse the command line safely and `subprocess`
to run the command without invoking a shell.  If the command or any
of its subcommands are not in the allowed list, a ValueError is
raised.

This implementation mitigates CWE‑707 by ensuring that only well‑formed,
explicitly permitted commands are executed, preventing injection
or accidental execution of dangerous code.
"""

import shlex
import subprocess
from typing import List

def filter_and_run_command(cmd_input: str, permitted_subcommands: List[str]) -> str:
    """
    Execute a command only if it matches the permitted subcommands.

    Parameters
    ----------
    cmd_input : str
        The raw command string to execute.
    permitted_subcommands : List[str]
        A list of subcommand names that are allowed (e.g. ['ls', 'cat']).

    Returns
    -------
    str
        The standard output of the command if it executes successfully.

    Raises
    ------
    ValueError
        If the command is empty, or if any part of it (including nested
        subcommands) is not in the permitted list.
    RuntimeError
        If the command fails to execute (non‑zero exit status).
    """
    if not cmd_input.strip():
        raise ValueError("Empty command is not allowed.")

    # Parse the command into a list of arguments safely.
    try:
        tokens = shlex.split(cmd_input, posix=True)
    except ValueError as e:   # Malformed command line
        raise ValueError(f"Malformed command: {e}") from e

    if not tokens:
        raise ValueError("Command parsing resulted in no tokens.")

    # Validate the main command and any sub‑commands (arguments that look like commands)
    for idx, token in enumerate(tokens):
        # Ignore simple options (start with '-' or '--') and numeric arguments
        if token.startswith('-'):
            continue
        if token.isdigit():
            continue

        # For the first token (the executable) we check against permitted list.
        if idx == 0:
            cmd_name = token
        else:
            # For subsequent tokens, treat them as potential subcommands only if they are not arguments.
            # Here we conservatively check every token that is not an option or number.
            cmd_name = token

        if cmd_name not in permitted_subcommands:
            raise ValueError(f"Command or subcommand '{cmd_name}' is not allowed.")

    # Execute the command without invoking a shell to avoid injection.
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=True,          # Raises CalledProcessError on non‑zero exit
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Command '{cmd_input}' failed with exit code {e.returncode}.\n"
            f"stderr: {e.stderr.strip()}"
        ) from e
    except FileNotFoundError as e:
        raise RuntimeError(f"Executable not found: {e}") from e

    return result.stdout.strip()

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    allowed = ["echo", "ls", "cat"]
    try:
        output = filter_and_run_command("echo Hello, World!", allowed)
        print(f"Command succeeded: {output}")
    except Exception as exc:
        print(f"Error: {exc}")