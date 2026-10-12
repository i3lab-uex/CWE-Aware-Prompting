import shlex
import subprocess
import os

def filtered_system_command(cmd: str, approved_cmd_list: list) -> str:
    """
    Execute a shell command only if all tokens are in the approved_cmd_list.

    Parameters
    ----------
    cmd : str
        The user-supplied command string.
    approved_cmd_list : list
        List of allowed subcommands (tokens). Each token in the command must be present
        in this list, otherwise a ValueError is raised.

    Returns
    -------
    str
        The combined stdout and stderr of the executed command, or an error message.

    Raises
    ------
    ValueError
        If any token in the command is not present in approved_cmd_list.
    """
    # Tokenise the user input safely
    try:
        tokens = shlex.split(cmd)
    except ValueError as exc:
        return f"Command parsing error: {exc}"

    if not tokens:
        return "No command supplied."

    # Validate each token
    for token in tokens:
        if token not in approved_cmd_list:
            raise ValueError(f"Disallowed subcommand: '{token}'")

    # Execute the command
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # We handle errors ourselves
        )
    except FileNotFoundError:
        return f"Command not found: {tokens[0]}"
    except Exception as exc:
        return f"Execution error: {exc}"

    # Combine stdout and stderr for the caller
    output = result.stdout + result.stderr
    return output if output else f"Command executed with exit code {result.returncode}"