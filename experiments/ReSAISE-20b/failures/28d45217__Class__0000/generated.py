import shlex
import subprocess
from typing import List


def validate_and_execute_command(
    input_command: str,
    permitted_subcommands: List[str]
) -> str:
    """
    Execute a shell command only if every subcommand token is in the
    permitted_subcommands list.

    Parameters:
        input_command (str): The raw command string supplied by the user.
        permitted_subcommands (List[str]): A list of tokens that are allowed.

    Returns:
        str: The command's stdout if executed successfully, or an error
             message if a forbidden subcommand is detected.

    Raises:
        ValueError: If the command or any token is not found in
                    permitted_subcommands.
    """
    # Split the input safely into tokens
    try:
        tokens = shlex.split(input_command)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command is not allowed.")

    # Validate each token against the whitelist
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Forbidden subcommand: {token}")

    # Execute the command securely (no shell expansion)
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # we handle non-zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {tokens[0]}") from exc
    except Exception as exc:
        raise ValueError(f"Execution failed: {exc}") from exc

    # Return stdout or stderr based on exit status
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Command failed with exit code {result.returncode}:\n{result.stderr.strip()}"