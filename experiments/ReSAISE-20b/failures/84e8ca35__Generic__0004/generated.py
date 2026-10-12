import os
import shlex
import subprocess
from typing import List


def restricted_command_executor(user_command: str, whitelist_commands: List[str]) -> str:
    """
    Execute a user-supplied shell command only if it is in the whitelist.

    Parameters
    ----------
    user_command : str
        The command string provided by the user.
    whitelist_commands : list of str
        A list containing the names of commands that are allowed to run.

    Returns
    -------
    str
        The stdout output from the executed command, or an error message if execution fails.

    Raises
    ------
    ValueError
        If the command or any of its arguments are not present in the whitelist.
    """
    # Split the command into tokens safely
    try:
        tokens = shlex.split(user_command)
    except ValueError as exc:  # malformed shell string
        return f"Invalid command syntax: {exc}"

    if not tokens:
        return "No command provided."

    # Validate every token against the whitelist
    for token in tokens:
        if token not in whitelist_commands:
            raise ValueError(f"Command or argument '{token}' is not allowed.")

    # Execute the command securely (no shell)
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as exc:
        # Return the stderr output if command fails
        return f"Command failed with exit code {exc.returncode}:\n{exc.stderr}"
    except FileNotFoundError:
        return f"Command not found: {tokens[0]}"

    # Return the stdout output
    return result.stdout

# Example usage (commented out):
# whitelist = ['echo', 'ls', 'pwd']
# print(restricted_command_executor("echo Hello World", whitelist))