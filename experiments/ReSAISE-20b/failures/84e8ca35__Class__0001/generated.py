import shlex
import subprocess
from typing import List

def restricted_command_executor(user_command: str, whitelist_commands: List[str]) -> str:
    """
    Execute a user-supplied shell command only if every token is present
    in the whitelist_commands list.

    Parameters:
        user_command (str): The command string supplied by the user.
        whitelist_commands (List[str]): A list of allowed subcommands.

    Returns:
        str: The combined stdout and stderr output of the executed command
             or an error message if execution fails.

    Raises:
        ValueError: If any token in the command is not in whitelist_commands.
    """
    # Tokenise the command safely
    try:
        tokens = shlex.split(user_command, posix=True)
    except ValueError as e:
        return f"Command parsing error: {e}"

    if not tokens:
        raise ValueError("Empty command is not allowed")

    # Ensure every token is whitelisted
    for token in tokens:
        if token not in whitelist_commands:
            raise ValueError(f"Disallowed command component: '{token}'")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # Do not raise on non-zero exit status
        )
    except Exception as e:
        return f"Execution error: {e}"

    # Combine stdout and stderr for a single string result
    output = result.stdout + result.stderr
    return output.strip()