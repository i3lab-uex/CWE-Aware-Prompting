#!/usr/bin/env python3
"""
Utility to execute a shell command only if it matches a whitelist of safe subcommands.

The function validates the command string using shlex to avoid shell injection
and ensures that each component of the parsed command is present in a list
of permitted subcommands.  If validation passes, it runs the command using
subprocess.run with `shell=False` to avoid invoking a shell.

CWE-707: This implementation ensures that the command is well‑formed and
only allowed tokens are executed, mitigating improper neutralization.
"""

import shlex
import subprocess
from typing import List

def validate_and_execute_command(
    shell_cmd: str,
    safe_subcommands: List[str]
) -> str:
    """
    Validate and execute a shell command.

    Parameters
    ----------
    shell_cmd : str
        The command string to be executed.
    safe_subcommands : List[str]
        A list of subcommand tokens considered safe and permitted.

    Returns
    -------
    str
        The standard output of the executed command, or an error message if
        validation fails.

    Raises
    ------
    ValueError
        If the command or any of its subcommands do not match the allowed list.
    """
    if not shell_cmd:
        raise ValueError("Empty command provided")

    # Split the command safely; this preserves quoted arguments.
    try:
        tokens = shlex.split(shell_cmd, posix=True)
    except ValueError as exc:
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("Command contains no executable")

    # Validate each token against the whitelist.
    for idx, token in enumerate(tokens):
        if token not in safe_subcommands:
            raise ValueError(
                f"Token '{token}' at position {idx} is not in the allowed list"
            )

    # Execute command without invoking a shell.
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False  # We'll handle non‑zero exit codes manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Executable not found: {tokens[0]}") from exc
    except Exception as exc:
        raise ValueError(f"Execution failed: {exc}") from exc

    if result.returncode != 0:
        # Return the stderr output as part of the error message.
        return f"Command failed with exit code {result.returncode}:\n{result.stderr}"

    return result.stdout


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     allowed = ["echo", "ls", "-l", "/tmp"]
#     try:
#         output = validate_and_execute_command("echo hello world", allowed)
#         print(output)
#     except ValueError as e:
#         print(f"Validation error: {e}")