import os
import shlex
import subprocess

def filtered_system_command(cmd: str, approved_cmd_list: list) -> str:
    """
    Execute a shell command only if all its components are in the approved list.

    Parameters
    ----------
    cmd : str
        The user-supplied command string.
    approved_cmd_list : list
        A list of permitted subcommands (including flags and arguments).

    Returns
    -------
    str
        Standard output of the command if executed successfully,
        otherwise an error message.

    Raises
    ------
    ValueError
        If any token in the command is not present in `approved_cmd_list`.
    """
    if not cmd.strip():
        return "Error: empty command"

    # Tokenise the command safely
    try:
        tokens = shlex.split(cmd)
    except ValueError as e:  # bad quoting, etc.
        return f"Error parsing command: {e}"

    # Ensure every token is approved
    for token in tokens:
        if token not in approved_cmd_list:
            raise ValueError(f"Disallowed command component: '{token}'")

    # Execute the command securely (no shell)
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,          # we handle non‑zero exit ourselves
        )
    except FileNotFoundError:
        return f"Error: command not found: {tokens[0]}"
    except Exception as e:
        return f"Execution error: {e}"

    # Combine stdout and stderr for the caller
    output = result.stdout + result.stderr

    if result.returncode != 0:
        return f"Command exited with code {result.returncode}:\n{output}"
    return output