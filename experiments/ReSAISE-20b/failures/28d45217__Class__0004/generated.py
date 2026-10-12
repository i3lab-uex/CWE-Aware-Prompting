import shlex
import subprocess

def validate_and_execute_command(input_command: str, permitted_subcommands: list) -> str:
    """
    Execute a shell command only if every token (subcommand) is in the permitted list.

    Parameters
    ----------
    input_command : str
        The command string supplied by the user.
    permitted_subcommands : list
        A collection of allowed subcommand tokens.

    Returns
    -------
    str
        The combined stdout and stderr of the executed command, or an error message.

    Raises
    ------
    ValueError
        If any token in the command is not present in `permitted_subcommands`.
    """
    # Tokenise safely
    try:
        tokens = shlex.split(input_command)
    except ValueError as exc:  # e.g., unmatched quotes
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command is not allowed.")

    # Validate each token
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Forbidden subcommand detected: '{token}'")

    # Execute the command safely (no shell expansion)
    try:
        completed = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False  # We handle non-zero return codes ourselves
        )
    except FileNotFoundError as exc:
        # The executable itself is missing
        raise ValueError(f"Command not found: {tokens[0]}") from exc

    # Prepare the output
    if completed.returncode == 0:
        return completed.stdout.strip()
    else:
        error_msg = f"Command failed with exit code {completed.returncode}:\n{completed.stderr.strip()}"
        return error_msg