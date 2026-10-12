import os
import shlex
import subprocess
from typing import List

def filtered_system_command(cmd: str, approved_cmd_list: List[str]) -> str:
    """
    Execute a shell command only if all tokens are present in approved_cmd_list.

    Parameters
    ----------
    cmd : str
        The user-supplied shell command to execute.
    approved_cmd_list : List[str]
        A list of allowed subcommands. Every token in the command must be
        contained in this list, otherwise a ValueError is raised.

    Returns
    -------
    str
        The stdout of the executed command or an error message if execution fails.

    Raises
    ------
    ValueError
        If any token in `cmd` is not found in `approved_cmd_list`.
    """
    # Tokenise the command safely (no shell expansion)
    try:
        tokens = shlex.split(cmd, posix=True)
    except ValueError as e:          # malformed input
        return f"Command parsing error: {e}"

    if not tokens:
        return "Empty command"

    # Ensure each token is approved
    for token in tokens:
        if token not in approved_cmd_list:
            raise ValueError(f"Command '{token}' is not allowed")

    # Execute the command securely (no shell=True)
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=True,          # raise CalledProcessError on non-zero exit
        )
    except subprocess.CalledProcessError as e:
        return f"Command failed with exit code {e.returncode}\n{e.stderr}"
    except FileNotFoundError:
        return f"Command not found: {tokens[0]}"
    except PermissionError:
        return f"Permission denied executing: {tokens[0]}"

    # Return stdout (or empty string if no output)
    return result.stdout.strip()