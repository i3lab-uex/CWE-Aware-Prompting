import os
import shlex
import subprocess
from typing import List

def execute_permitted_command(input_command: str, approved_commands: List[str]) -> str:
    """
    Execute a shell command only if every token in the command is present
    in the list of approved subcommands.

    Parameters:
        input_command (str): The user supplied command string.
        approved_commands (List[str]): A list of allowed command tokens.

    Returns:
        str: The combined stdout and stderr from the executed command
             if successful, otherwise an error message.

    Raises:
        ValueError: If any token in the command is not in approved_commands.
    """
    # Split the input into tokens safely
    try:
        cmd_tokens = shlex.split(input_command, posix=True)
    except ValueError as e:
        return f"Command parsing error: {e}"

    if not cmd_tokens:
        return "No command provided."

    # Validate each token against the approved list
    for token in cmd_tokens:
        if token not in approved_commands:
            raise ValueError(f"Unauthorized command component: '{token}'")

    # Execute the command without using shell=True for safety
    try:
        result = subprocess.run(
            cmd_tokens,
            capture_output=True,
            text=True,
            check=False  # We'll handle non-zero exit codes ourselves
        )
    except FileNotFoundError:
        return f"Command not found: {cmd_tokens[0]}"
    except Exception as e:
        return f"Execution error: {e}"

    # Combine stdout and stderr for the caller
    output = result.stdout + result.stderr

    if result.returncode != 0:
        return f"Command exited with status {result.returncode}:\n{output}"

    return output