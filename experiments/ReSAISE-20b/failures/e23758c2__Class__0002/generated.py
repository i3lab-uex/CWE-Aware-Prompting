import shlex
import subprocess
from typing import List


def validate_and_execute_command(
    input_command: str, permitted_subcommands: List[str]
) -> str:
    """
    Execute a shell command only if all of its subcommands are in the
    permitted_subcommands list.

    Parameters:
        input_command (str): The full command string to be executed.
        permitted_subcommands (List[str]): List of allowed subcommand tokens.

    Returns:
        str: The stdout produced by the command.

    Raises:
        ValueError: If any token in the parsed command is not in
                    permitted_subcommands or if the command fails.
    """
    # Split the command safely into tokens
    try:
        tokens = shlex.split(input_command)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("No command provided")

    # Verify each token is permitted
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Disallowed subcommand: {token!r}")

    # Execute the command without invoking a shell
    result = subprocess.run(
        tokens,
        capture_output=True,
        text=True,
        check=False,  # We'll raise on non-zero exit ourselves
    )

    if result.returncode != 0:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command failed with exit code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout