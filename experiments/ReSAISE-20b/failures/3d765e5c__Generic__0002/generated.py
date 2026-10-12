import os
import shlex
import subprocess
from typing import List


def filtered_system_command(cmd: str, approved_cmd_list: List[str]) -> str:
    """
    Execute a system command only if all of its tokens are present in
    `approved_cmd_list`.  The function uses a safe, non‑shell execution path.

    Parameters
    ----------
    cmd : str
        The user supplied shell command to execute.
    approved_cmd_list : List[str]
        A list of subcommands that are permitted.  Each token in the
        command must be present in this list.

    Returns
    -------
    str
        The combined stdout and stderr of the executed command, or an error
        message if execution fails.

    Raises
    ------
    ValueError
        If any token in `cmd` is not found in `approved_cmd_list`.
    """
    # Tokenize the command safely
    tokens = shlex.split(cmd)

    if not tokens:
        raise ValueError("Empty command provided")

    # Verify each token against the approved list
    for token in tokens:
        if token not in approved_cmd_list:
            raise ValueError(f"Disallowed command or argument: '{token}'")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as e:
        return f"Command not found: {e}"
    except Exception as e:
        return f"Execution error: {e}"

    # Combine stdout and stderr for the caller
    output = result.stdout + result.stderr
    return output.strip() or "Command executed with no output."