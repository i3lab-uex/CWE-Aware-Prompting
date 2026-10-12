import shlex
import subprocess

def filter_and_run_os_command(exec_command: str, whitelisted_subcommands: list) -> str:
    """
    Execute a shell command only if every token in the command is present
    in ``whitelisted_subcommands``.  The function uses a safe execution
    path (no shell) and returns the command output or an error message.

    Parameters:
        exec_command (str): The user supplied command string.
        whitelisted_subcommands (list[str]): Allowed tokens.

    Returns:
        str: Standard output of the command or an error message.

    Raises:
        ValueError: If any token in ``exec_command`` is not in
                    ``whitelisted_subcommands``.
    """
    # Split the command safely into tokens (handles quotes, escapes)
    try:
        tokens = shlex.split(exec_command)
    except ValueError as exc:
        # Raised if the command string is malformed
        raise ValueError(f"Malformed command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command")

    # Verify that each token is in the whitelist
    for token in tokens:
        if token not in whitelisted_subcommands:
            raise ValueError(f"Forbidden subcommand or argument: {token}")

    # Execute the command without using a shell to avoid injection
    try:
        completed = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # We handle errors ourselves
        )
    except FileNotFoundError as exc:
        return f"Command not found: {tokens[0]}"
    except Exception as exc:
        return f"Execution failed: {exc}"

    # Return stdout if successful, else stderr
    if completed.returncode == 0:
        return completed.stdout.strip()
    else:
        return f"Error ({completed.returncode}): {completed.stderr.strip()}"