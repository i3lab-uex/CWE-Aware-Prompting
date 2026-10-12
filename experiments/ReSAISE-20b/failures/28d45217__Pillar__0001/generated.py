import shlex
import subprocess
from typing import List


def validate_and_execute_command(
    input_command: str,
    permitted_subcommands: List[str]
) -> str:
    """
    Execute a shell command only if every subcommand token is present in
    *permitted_subcommands*.  The function uses a safe parsing approach via
    shlex and executes the command with subprocess.run without invoking a shell.
    
    Parameters
    ----------
    input_command : str
        The raw command string supplied by the user.
    permitted_subcommands : List[str]
        A list of strings that represent allowed subcommand tokens.  Every
        token obtained from shlex.split(input_command) must be in this list.

    Returns
    -------
    str
        The standard output of the command if it executed successfully.
        If the command fails, its standard error is returned.

    Raises
    ------
    ValueError
        If the command string is empty, or if any token from the parsed
        command is not in *permitted_subcommands*.
    """
    # 1. Sanity check for empty command
    if not input_command.strip():
        raise ValueError("Empty command is not allowed.")

    # 2. Tokenize the command safely (no shell expansion)
    try:
        tokens = shlex.split(input_command, posix=True)
    except ValueError as exc:  # malformed quoting etc.
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Command could not be parsed into tokens.")

    # 3. Validate each token against the permitted list
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(
                f"Forbidden subcommand detected: '{token}'. "
                "Only the following subcommands are allowed: "
                f"{', '.join(permitted_subcommands)}."
            )

    # 4. Execute the command safely (no shell=True)
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # we will handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Executable not found: {tokens[0]}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    # 5. Return stdout on success, else stderr with error details
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        # Include the return code for debugging
        error_msg = (
            f"Command failed with exit status {result.returncode}.\n"
            f"{result.stderr.strip()}"
        )
        return error_msg