import shlex
import subprocess
from typing import List

def validate_and_execute_command(
    input_command: str,
    permitted_subcommands: List[str]
) -> str:
    """
    Execute a shell command only if all subcommands are permitted.

    Parameters
    ----------
    input_command : str
        The command string supplied by the user.
    permitted_subcommands : list[str]
        A list of subcommand names that are allowed.

    Returns
    -------
    str
        The combined stdout and stderr of the executed command,
        or an error message if execution was not allowed.

    Raises
    ------
    ValueError
        If the command is empty or any subcommand is not in
        ``permitted_subcommands``.
    """
    # Trim whitespace and ensure the command is not empty
    stripped_cmd = input_command.strip()
    if not stripped_cmd:
        raise ValueError("No command provided.")

    # Safely split the command into tokens
    try:
        tokens = shlex.split(stripped_cmd)
    except ValueError as exc:
        # shlex can raise if the input is malformed
        raise ValueError(f"Malformed command: {exc}") from exc

    # Validate each subcommand against the permitted list
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Forbidden subcommand: '{token}'")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False
        )
    except FileNotFoundError as exc:
        # The executable was not found on the system
        raise ValueError(f"Command not found: {tokens[0]}") from exc

    # Combine stdout and stderr for the return value
    output = result.stdout + result.stderr
    if not output:
        # Provide a minimal message when there is no output
        output = "<no output>"
    return output

# Example usage:
if __name__ == "__main__":
    allowed = ["echo", "ls", "pwd"]
    try:
        print(validate_and_execute_command("echo Hello, World!", allowed))
    except ValueError as e:
        print(f"Error: {e}")