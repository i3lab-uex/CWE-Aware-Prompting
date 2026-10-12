import os
import shlex
import subprocess
from typing import List


def filtered_system_command(cmd: str, approved_cmd_list: List[str]) -> str:
    """
    Execute a system command only if every token in the supplied command
    string is present in *approved_cmd_list*.

    Parameters
    ----------
    cmd : str
        The user‑supplied shell command to be executed.
    approved_cmd_list : list[str]
        A collection of permitted subcommands. Every token that appears
        in *cmd* must match one element of this list.

    Returns
    -------
    str
        The combined stdout and stderr output from the command if it runs
        successfully, otherwise an error message.

    Raises
    ------
    ValueError
        If any token in *cmd* is not found in *approved_cmd_list*.
    """
    # Tokenise the command safely (no shell expansion)
    try:
        tokens = shlex.split(cmd, posix=True)
    except ValueError as exc:   # malformed shell string
        return f"Invalid command syntax: {exc}"

    if not tokens:
        return "No command to execute."

    # Validate each token
    for token in tokens:
        if token not in approved_cmd_list:
            raise ValueError(
                f"Command '{token}' is not in the list of approved subcommands."
            )

    # Execute the command without invoking a shell for safety
    try:
        completed = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # we handle errors ourselves
        )
    except OSError as exc:
        return f"Execution failed: {exc}"

    # Build the result string
    output = completed.stdout.strip()
    error = completed.stderr.strip()

    if completed.returncode != 0:
        return f"Command failed with exit code {completed.returncode}:\n{error}"
    if error:
        return f"Command succeeded with warnings:\n{output}\nSTDERR:\n{error}"
    return output