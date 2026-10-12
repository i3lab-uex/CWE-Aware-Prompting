import os
import shlex
import subprocess
from typing import List

def filter_and_run_os_command(exec_command: str, whitelisted_subcommands: List[str]) -> str:
    """
    Execute a shell command only if all sub‑components are in the whitelist.

    Parameters
    ----------
    exec_command : str
        The command string requested by the caller.
    whitelisted_subcommands : List[str]
        A list of sub‑command names that are allowed to be executed.

    Returns
    -------
    str
        The combined stdout and stderr from the command execution, or an error message.

    Raises
    ------
    ValueError
        If the command is empty or any sub‑command is not in the whitelist.
    """
    # Strip whitespace and validate non-empty
    command_str = exec_command.strip()
    if not command_str:
        raise ValueError("No command provided")

    # Safely split the command into tokens
    try:
        tokens = shlex.split(command_str)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    # Validate each token against the whitelist
    for token in tokens:
        if token not in whitelisted_subcommands:
            raise ValueError(f"Forbidden subcommand: {token}")

    # Execute the command and capture output
    result = subprocess.run(
        tokens,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,  # decode bytes to str
    )

    return result.stdout

# Example usage:
if __name__ == "__main__":
    whitelist = ["echo", "ls", "-l", "/tmp"]
    try:
        output = filter_and_run_os_command("echo hello world", whitelist)
        print(output)
    except ValueError as e:
        print(f"Command rejected: {e}")