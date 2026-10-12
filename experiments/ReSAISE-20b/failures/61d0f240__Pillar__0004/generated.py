import os
import shlex
import subprocess
from typing import List

def execute_permitted_command(input_command: str, approved_commands: List[str]) -> str:
    """
    Execute a user-supplied shell command only if all its tokens are in the
    approved_commands list.

    Parameters:
        input_command (str): The raw command string supplied by the user.
        approved_commands (List[str]): A list of subcommands that are allowed to run.

    Returns:
        str: The standard output from the command if executed successfully,
             otherwise the error message.

    Raises:
        ValueError: If any token in the command is not present in approved_commands.
    """
    # Split the input command into tokens safely
    try:
        tokens = shlex.split(input_command)
    except ValueError as exc:   # malformed quoting etc.
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command is not allowed")

    # Verify every token against the approved list
    for token in tokens:
        if token not in approved_commands:
            raise ValueError(f"Command '{token}' is not permitted")

    # Execute the command without invoking a shell (mitigates shell injection)
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # we handle non-zero exit codes manually
        )
    except FileNotFoundError as exc:
        return f"Command not found: {exc}"
    except Exception as exc:  # pragma: no cover
        return f"Execution failed: {exc}"

    # Return stdout or stderr depending on exit status
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        # Include stderr to help diagnose issues
        return f"Error (code {result.returncode}):\n{result.stderr.strip()}"