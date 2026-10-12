import shlex
import subprocess

def execute_permitted_command(input_command: str, approved_commands: list[str]) -> str:
    """
    Execute a shell command only if every token in the command is present
    in `approved_commands`. Raises ValueError otherwise.

    Parameters:
        input_command (str): The user-supplied command to run.
        approved_commands (list[str]): List of allowed subcommands.

    Returns:
        str: Combined stdout and stderr from the executed command, or an
             error message if execution fails.

    Raises:
        ValueError: If any token in the command is not approved.
    """
    if not isinstance(input_command, str):
        raise ValueError("Command must be a string")

    # Tokenize the command safely
    try:
        tokens = shlex.split(input_command)
    except ValueError as exc:
        # shlex could raise if the command is malformed
        raise ValueError(f"Malformed command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command")

    # Validate each token against the approved list
    for token in tokens:
        if token not in approved_commands:
            raise ValueError(f"Unauthorized subcommand: {token!r}")

    # Execute the command securely (no shell expansion)
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # Don't raise on non-zero exit status
        )
    except Exception as exc:
        return f"Execution failed: {exc}"

    # Combine stdout and stderr for the caller
    output = result.stdout + result.stderr
    return output.strip()