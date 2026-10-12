import os
import shlex
import subprocess
from typing import List


def restricted_command_executor(user_command: str, whitelist_commands: List[str]) -> str:
    """
    Execute a user supplied shell command after validating that every token
    (command and arguments) is present in the provided whitelist.

    Parameters:
        user_command (str): The raw command string supplied by a user.
        whitelist_commands (List[str]): List of permitted tokens.

    Returns:
        str: Combined stdout and stderr from the executed command,
             or an error message if execution failed.

    Raises:
        ValueError: If any token in the command is not found in
                    ``whitelist_commands``.
    """
    if not user_command:
        raise ValueError("No command provided")

    # Tokenize the command safely (no shell expansion)
    try:
        tokens = shlex.split(user_command, posix=True)
    except ValueError as exc:
        # ``shlex`` failed to parse the command (e.g., unmatched quotes)
        raise ValueError(f"Malformed command: {exc}") from exc

    # Validate every token against the whitelist
    missing = [t for t in tokens if t not in whitelist_commands]
    if missing:
        raise ValueError(
            f"Unauthorized token(s) detected: {', '.join(missing)}"
        )

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # We handle non‑zero exit codes manually
        )
    except FileNotFoundError as exc:
        # Command binary not found on the system
        return f"Command not found: {exc}"
    except Exception as exc:
        # Generic execution error
        return f"Execution failed: {exc}"

    output = result.stdout + ("\n" if result.stdout and result.stderr else "") + result.stderr

    # If the command failed, include a clear message
    if result.returncode != 0:
        output = f"Command exited with status {result.returncode}:\n{output}"

    return output.strip()