import shlex
import subprocess

def validate_and_execute_command(input_command: str, permitted_subcommands: list) -> str:
    """
    Execute a shell command only if all sub‑components are permitted.

    Parameters
    ----------
    input_command : str
        The raw command string supplied by the user.
    permitted_subcommands : list
        A list of sub‑command strings that are allowed. Each token after the
        primary command must be present in this list.

    Returns
    -------
    str
        The combined stdout and stderr from the executed command.

    Raises
    ------
    ValueError
        If `input_command` is empty or if any token after the primary command
        is not in `permitted_subcommands`.
    """
    if not input_command or not input_command.strip():
        raise ValueError("Command must not be empty")

    # Safely split the command into tokens
    try:
        parts = shlex.split(input_command)
    except ValueError as exc:  # e.g. unmatched quotes
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not parts:
        raise ValueError("Command contains no executable")

    # Validate sub‑commands (all tokens after the first)
    for token in parts[1:]:
        if token not in permitted_subcommands:
            raise ValueError(f"Disallowed subcommand: {token}")

    # Execute without invoking the shell to avoid injection risks
    result = subprocess.run(
        parts,
        capture_output=True,
        text=True,
        check=False,  # we will handle errors ourselves
    )

    output = result.stdout + result.stderr

    if result.returncode != 0:
        raise ValueError(f"Command failed with exit code {result.returncode}:\n{output}")

    return output