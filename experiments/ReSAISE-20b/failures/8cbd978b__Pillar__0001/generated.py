import shlex
import subprocess
from typing import List


def filter_and_run_os_command(
    exec_command: str,
    whitelisted_subcommands: List[str],
) -> str:
    """
    Execute a shell command only if all of its subcommands are whitelisted.

    Parameters
    ----------
    exec_command : str
        The full command string the user wishes to execute.
    whitelisted_subcommands : List[str]
        A list of allowed subcommand tokens. Every token produced by
        shlex.split(exec_command) must appear in this list.

    Returns
    -------
    str
        The combined stdout and stderr of the executed command.

    Raises
    ------
    ValueError
        If any token in exec_command is not present in the whitelist.
    """
    # Safely split the command into tokens
    try:
        cmd_tokens = shlex.split(exec_command, posix=True)
    except ValueError as exc:
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not cmd_tokens:
        raise ValueError("Empty command is not allowed.")

    # Validate every token against the whitelist
    for token in cmd_tokens:
        if token not in whitelisted_subcommands:
            raise ValueError(f"Forbidden subcommand: '{token}'")

    # Execute the command without invoking a shell to avoid injection
    try:
        result = subprocess.run(
            cmd_tokens,
            capture_output=True,
            text=True,
            check=False,  # We will handle non-zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {exc}") from exc

    # Combine stdout and stderr for the caller
    output = result.stdout + result.stderr
    return output


# Example usage (commented out):
#
# if __name__ == "__main__":
#     whitelist = ["echo", "ls", "-l", "/tmp"]
#     try:
#         print(filter_and_run_os_command("echo hello world", whitelist))
#     except ValueError as e:
#         print(f"Error: {e}")