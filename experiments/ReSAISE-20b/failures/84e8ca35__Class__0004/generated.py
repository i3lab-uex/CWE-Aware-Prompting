import os
import shlex
import subprocess

def restricted_command_executor(user_command: str, whitelist_commands: list) -> str:
    """
    Execute a shell command only if all its tokens are present in the whitelist.

    Parameters
    ----------
    user_command : str
        The command string supplied by the user.
    whitelist_commands : list[str]
        A list of allowed subcommands. Every token in the user command must be
        present in this list; otherwise a ValueError is raised.

    Returns
    -------
    str
        The stdout of the executed command if successful, or a descriptive error
        message if execution fails.

    Raises
    ------
    ValueError
        If any token in the command is not part of ``whitelist_commands``.
    """
    # Split the user input into individual tokens in a shell‑safe way
    try:
        tokens = shlex.split(user_command)
    except ValueError as exc:  # malformed quoting
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command is not allowed")

    # Verify every token against the whitelist
    for token in tokens:
        if token not in whitelist_commands:
            raise ValueError(f"Command '{token}' is not allowed")

    # Execute the command safely without invoking a shell
    try:
        completed = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # we handle non‑zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        return f"Command not found: {exc}"
    except PermissionError as exc:
        return f"Permission denied executing command: {exc}"

    # Return stdout or stderr depending on success
    if completed.returncode == 0:
        return completed.stdout.strip()
    else:
        return (
            f"Command failed with exit code {completed.returncode}\n"
            f"{completed.stderr.strip()}"
        )