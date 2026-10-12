import shlex
import subprocess
from typing import List

def execute_command_with_restrictions(cmd: str, approved_subcommands: List[str]) -> str:
    """
    Execute a shell command only if it contains approved subcommands.

    Parameters
    ----------
    cmd : str
        The command string to execute.
    approved_subcommands : list[str]
        List of subcommand names that are considered safe and permitted.

    Returns
    -------
    str
        The stdout of the executed command if successful, otherwise an error message.

    Raises
    ------
    ValueError
        If the command or any of its subcommands are not in the approved list.
    """
    # Parse the command into a list of arguments safely
    try:
        args = shlex.split(cmd)
    except ValueError as exc:
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not args:
        raise ValueError("Empty command provided")

    # The first token is the executable; check it against approved subcommands
    if args[0] not in approved_subcommands:
        raise ValueError(f"Command '{args[0]}' is not allowed")

    # Optionally, you can also check each argument if needed
    # for token in args[1:]:
    #     if token not in approved_subcommands:
    #         raise ValueError(f"Argument '{token}' is not allowed")

    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False  # We handle non-zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Executable not found: {args[0]}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        return f"Command failed with exit code {result.returncode}:\n{result.stderr.strip()}"

    return result.stdout.strip()