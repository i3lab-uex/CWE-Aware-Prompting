import os
import shlex
import subprocess
from typing import List


def execute_permitted_command(input_command: str, approved_commands: List[str]) -> str:
    """
    Execute a user‑supplied shell command only if all of its tokens are in the
    approved_commands list.

    Parameters
    ----------
    input_command : str
        The command string supplied by the user.
    approved_commands : list[str]
        A collection of subcommands that are allowed to run.

    Returns
    -------
    str
        The command's stdout and stderr output if executed successfully,
        otherwise an error message.

    Raises
    ------
    ValueError
        If any token in the command is not present in approved_commands.
    """
    # Split the input into individual tokens safely
    try:
        tokens = shlex.split(input_command)
    except ValueError as exc:   # malformed command
        return f"Command parsing error: {exc}"

    if not tokens:
        return "No command provided."

    # Verify that every token is approved
    for token in tokens:
        if token not in approved_commands:
            raise ValueError(f"Disallowed command part: {token!r}")

    # Execute the command without using a shell to avoid injection
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # don't raise on non‑zero exit status
        )
    except FileNotFoundError:
        return f"Command not found: {tokens[0]!r}"
    except Exception as exc:
        return f"Execution failed: {exc}"

    # Combine stdout and stderr for a single string result
    output = result.stdout + ("\n" if result.stdout and result.stderr else "") + result.stderr
    return output.strip() or f"[{tokens[0]} exited with code {result.returncode}]"