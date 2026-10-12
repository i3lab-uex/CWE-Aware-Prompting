import shlex
import subprocess
from typing import List


def execute_permitted_command(
    input_command: str, approved_commands: List[str]
) -> str:
    """
    Execute a shell command after ensuring all its tokens are in the
    approved_commands list.

    Parameters
    ----------
    input_command : str
        The command string supplied by the user.
    approved_commands : list[str]
        A collection of permitted subcommands that may appear in the command.

    Returns
    -------
    str
        The stdout of the executed command, or an error message.

    Raises
    ------
    ValueError
        If any token in the command is not present in approved_commands.
    """
    # Tokenise the input command safely
    try:
        tokens = shlex.split(input_command)
    except ValueError as exc:
        return f"Invalid command syntax: {exc}"

    # Validate each token
    for token in tokens:
        if token not in approved_commands:
            raise ValueError(
                f"Command '{token}' is not permitted. "
                f"Allowed commands: {approved_commands}"
            )

    # Execute the command
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # We handle errors ourselves
        )
    except OSError as exc:
        return f"Execution failed: {exc}"

    # Return stdout or stderr based on exit status
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        # Include both stdout and stderr for debugging
        error_msg = (
            f"Command exited with code {result.returncode}\n"
            f"stdout:\n{result.stdout.strip()}\n"
            f"stderr:\n{result.stderr.strip()}"
        )
        return error_msg