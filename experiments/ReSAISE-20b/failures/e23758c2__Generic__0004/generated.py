import shlex
import subprocess

def validate_and_execute_command(input_command: str, permitted_subcommands: list) -> str:
    """
    Execute a shell command only if every token in the command is present
    in `permitted_subcommands`.

    Parameters
    ----------
    input_command : str
        The command string to be executed.
    permitted_subcommands : list[str]
        A list of tokens that are allowed in the command.

    Returns
    -------
    str
        The standard output of the executed command.

    Raises
    ------
    ValueError
        If any token in `input_command` is not found in `permitted_subcommands`.
    """
    # Break the command into tokens safely
    try:
        tokens = shlex.split(input_command)
    except ValueError as exc:  # malformed quoting
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command")

    # Validate each token against the permitted list
    invalid = [t for t in tokens if t not in permitted_subcommands]
    if invalid:
        raise ValueError(f"Invalid subcommand(s) detected: {', '.join(invalid)}")

    # Execute the command without using a shell to avoid injection
    result = subprocess.run(
        tokens,
        capture_output=True,
        text=True,
        check=False  # we want to return output even if non-zero exit
    )

    # Combine stdout and stderr for debugging purposes
    output = result.stdout.strip()
    error  = result.stderr.strip()

    if error:
        # Append stderr to output so the caller can see it
        output = f"{output}\n{error}".strip()

    return output