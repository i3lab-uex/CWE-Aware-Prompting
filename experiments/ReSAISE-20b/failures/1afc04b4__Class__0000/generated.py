import shlex
import subprocess
from typing import List


def run_shell_command_with_filters(command: str, allowed_subcommands_list: List[str]) -> str:
    """
    Execute a shell command after validating that the subcommand is in an allowed list.

    Parameters
    ----------
    command : str
        The full shell command to execute.
    allowed_subcommands_list : list[str]
        List of permitted subcommand names (the first argument after the main command).

    Returns
    -------
    str
        The standard output of the executed command.

    Raises
    ------
    ValueError
        If the command is empty, contains disallowed subcommands,
        or if execution fails.
    """
    if not command.strip():
        raise ValueError("Empty command is not allowed")

    # Safely split the command into arguments
    try:
        parts = shlex.split(command)
    except ValueError as exc:   # malformed quoting
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if len(parts) < 2:
        raise ValueError("Command must contain at least a main command and one subcommand")

    # The first element is the executable; we only check the second (subcommand)
    subcommand = parts[1]
    if subcommand not in allowed_subcommands_list:
        raise ValueError(f"Disallowed subcommand: {subcommand}")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            parts,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
    except subprocess.CalledProcessError as exc:
        raise ValueError(f"Command failed with exit code {exc.returncode}: {exc.output}") from exc

    return result.stdout