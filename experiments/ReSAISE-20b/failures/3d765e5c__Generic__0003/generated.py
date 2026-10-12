import shlex
import subprocess
from typing import List


def filtered_system_command(cmd: str, approved_cmd_list: List[str]) -> str:
    """
    Execute a shell command after verifying that all tokens are approved.

    Parameters
    ----------
    cmd : str
        The user-supplied shell command.
    approved_cmd_list : List[str]
        A list of subcommands that are allowed to run.

    Returns
    -------
    str
        The combined stdout and stderr from the command execution, or an error message.

    Raises
    ------
    ValueError
        If any token in the command is not present in `approved_cmd_list`.
    """
    # Split the command safely into tokens
    try:
        tokens = shlex.split(cmd)
    except ValueError as exc:  # pragma: no cover
        return f"Invalid command syntax: {exc}"

    if not tokens:
        raise ValueError("Empty command is not allowed.")

    # Ensure each token is approved
    for token in tokens:
        if token not in approved_cmd_list:
            raise ValueError(f"Command '{token}' is not authorized.")

    # Execute the command
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # We handle errors manually
        )
    except FileNotFoundError as exc:  # pragma: no cover
        return f"Command not found: {exc}"
    except Exception as exc:  # pragma: no cover
        return f"Execution failed: {exc}"

    output = result.stdout + result.stderr
    if not output:
        return "(no output)"
    return output.strip()