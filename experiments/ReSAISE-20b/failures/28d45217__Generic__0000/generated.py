import shlex
import subprocess

def validate_and_execute_command(input_command: str, permitted_subcommands: list[str]) -> str:
    """
    Execute a shell command only if all tokens are in the permitted_subcommands list.

    Parameters
    ----------
    input_command : str
        The command string to be executed.
    permitted_subcommands : list[str]
        List of allowed tokens (e.g., command names, subcommands, arguments).

    Returns
    -------
    str
        The standard output of the command if it succeeds, or an error message.

    Raises
    ------
    ValueError
        If the command is empty or any token is not in the permitted_subcommands list.
    """
    # Strip and check for empty input
    stripped_cmd = input_command.strip()
    if not stripped_cmd:
        raise ValueError("No command provided.")

    # Safely split the command into tokens
    try:
        tokens = shlex.split(stripped_cmd)
    except ValueError as e:   # e.g., unmatched quotes
        raise ValueError(f"Invalid command syntax: {e}")

    # Validate each token against the allowed list
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Forbidden subcommand or argument: '{token}'")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False  # we handle non-zero exit codes ourselves
        )
    except FileNotFoundError:
        return f"Command not found: {tokens[0]}"

    # Return stdout or stderr based on exit status
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        # Include stderr in the error message
        return f"Command failed with exit code {result.returncode}:\n{result.stderr.strip()}"