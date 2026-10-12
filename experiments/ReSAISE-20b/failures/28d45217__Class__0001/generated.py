import shlex
import subprocess

def validate_and_execute_command(input_command: str, permitted_subcommands: list) -> str:
    """
    Execute a shell command only if all subcommands are in the permitted list.

    Parameters
    ----------
    input_command : str
        The command string to be executed.
    permitted_subcommands : list
        A list of allowed subcommand tokens.

    Returns
    -------
    str
        The command's stdout if successful, otherwise an error message.

    Raises
    ------
    ValueError
        If any subcommand token is not in the permitted list.
    """
    # Split command into tokens safely
    try:
        tokens = shlex.split(input_command)
    except ValueError as e:
        raise ValueError(f"Failed to parse command: {e}") from None

    if not tokens:
        raise ValueError("Empty command provided")

    # Validate each token against the permitted list
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Forbidden subcommand detected: '{token}'")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # we handle errors ourselves
        )
    except FileNotFoundError as e:
        return f"Command not found: {e}"
    except Exception as e:
        return f"Execution error: {e}"

    if result.returncode != 0:
        return (
            f"Command failed with exit code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout.strip()