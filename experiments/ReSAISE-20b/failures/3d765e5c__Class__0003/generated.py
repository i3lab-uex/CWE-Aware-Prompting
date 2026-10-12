import os
import shlex
import subprocess
from typing import List

def filtered_system_command(cmd: str, approved_cmd_list: List[str]) -> str:
    """
    Execute a shell command only if all tokens are present in the approved list.

    Parameters
    ----------
    cmd : str
        The user-supplied command string.
    approved_cmd_list : list[str]
        List of allowed subcommands (tokens).

    Returns
    -------
    str
        Standard output of the command if successful, otherwise an error message.

    Raises
    ------
    ValueError
        If any token in the command is not in `approved_cmd_list`.
    RuntimeError
        If the underlying subprocess fails to execute.
    """
    # Tokenise command safely using shlex
    try:
        tokens = shlex.split(cmd, posix=True)
    except ValueError as e:  # shlex can raise on malformed input
        return f"Command parsing error: {e}"

    if not tokens:
        return "Empty command"

    # Ensure every token is approved
    for t in tokens:
        if t not in approved_cmd_list:
            raise ValueError(f"Command token '{t}' is not allowed")

    # Execute without invoking the shell to avoid injection
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False  # We'll handle non-zero exit ourselves
        )
    except FileNotFoundError:
        return f"Command not found: {tokens[0]}"
    except Exception as exc:
        return f"Execution failed: {exc}"

    # Return stdout and stderr combined for transparency
    output = result.stdout.strip()
    error_output = result.stderr.strip()

    if result.returncode != 0:
        return f"Command exited with code {result.returncode}\nError: {error_output}"
    if error_output:
        return f"Command executed but produced stderr:\n{error_output}\nOutput:\n{output}"
    return output