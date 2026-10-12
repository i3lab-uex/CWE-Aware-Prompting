import shlex
import subprocess

def execute_permitted_command(input_command: str, approved_commands: list) -> str:
    """
    Execute a user‑supplied command only if every token is in the list of
    approved subcommands.

    Parameters
    ----------
    input_command : str
        The raw command string supplied by the user.
    approved_commands : list[str]
        A list of subcommand names that are considered safe.

    Returns
    -------
    str
        The command's stdout on success, or the stderr if it fails.

    Raises
    ------
    ValueError
        If any token in the command is not present in ``approved_commands``.
    """
    # Tokenise the command using shlex for safe parsing
    try:
        tokens = shlex.split(input_command, posix=True)
    except ValueError as exc:
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command")

    # Verify every token against the approved list
    for token in tokens:
        if token not in approved_commands:
            raise ValueError(f"Disallowed command part: {token!r}")

    # Execute the command without a shell to avoid injection
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # we handle errors ourselves
        )
    except OSError as exc:
        return f"Execution failed: {exc}"

    # Return stdout on success; otherwise stderr
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Command failed with exit code {result.returncode}:\n{result.stderr.strip()}"