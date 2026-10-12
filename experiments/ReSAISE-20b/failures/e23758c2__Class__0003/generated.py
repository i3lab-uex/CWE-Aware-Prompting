import shlex
import subprocess

def validate_and_execute_command(input_command: str, permitted_subcommands: list) -> str:
    """
    Execute a shell command only if all its tokens are in the permitted_subcommands list.

    Parameters
    ----------
    input_command : str
        The command string the user wants to execute.
    permitted_subcommands : list[str]
        A collection of allowed command tokens.

    Returns
    -------
    str
        The stdout produced by the executed command.

    Raises
    ------
    ValueError
        If any token in the parsed command is not present in permitted_subcommands.
    """
    # Parse the command safely into a list of tokens
    try:
        tokens = shlex.split(input_command)
    except ValueError as exc:  # malformed quoting, etc.
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command provided")

    # Validate each token against the permitted list
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Command contains disallowed subcommand: '{token}'")

    # Execute the command without invoking a shell to avoid injection
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=True  # Raise CalledProcessError on non-zero exit
        )
    except subprocess.CalledProcessError as exc:
        # Include stderr in the exception message for debugging
        raise RuntimeError(
            f"Command '{input_command}' failed with exit code {exc.returncode}:\n{exc.stderr}"
        ) from exc

    return result.stdout