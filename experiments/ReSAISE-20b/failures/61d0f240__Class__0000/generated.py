import os
import shlex
import subprocess
from typing import List

def execute_permitted_command(input_command: str, approved_commands: List[str]) -> str:
    """
    Execute a user-supplied command only if all its tokens are in the approved list.

    Parameters
    ----------
    input_command : str
        The raw shell command string supplied by the user.
    approved_commands : list[str]
        A collection of subcommands that are allowed to run.

    Returns
    -------
    str
        The combined stdout and stderr of the executed command.

    Raises
    ------
    ValueError
        If any token in `input_command` is not present in `approved_commands`.
    """
    # Tokenise the command safely (no shell expansion)
    tokens = shlex.split(input_command)

    # Ensure each token is explicitly allowed
    for token in tokens:
        if token not in approved_commands:
            raise ValueError(f"Command component '{token}' is not permitted")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,   # we handle non-zero exit codes ourselves
        )
    except Exception as exc:
        return f"Execution failed: {exc}"

    # Combine stdout and stderr for a single string result
    output = result.stdout + result.stderr

    return output.strip()