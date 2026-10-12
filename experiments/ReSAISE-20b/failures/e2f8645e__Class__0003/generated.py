import shlex
import subprocess
from typing import List

def execute_command_with_restrictions(cmd: str, approved_subcommands: List[str]) -> str:
    """
    Execute a shell command only if all subcommands are in the approved list.

    Parameters
    ----------
    cmd : str
        The command to execute.
    approved_subcommands : List[str]
        A list of subcommand names that are considered safe.

    Returns
    -------
    str
        The command's standard output if execution succeeds, otherwise an error message.

    Raises
    ------
    ValueError
        If the command is empty or any subcommand is not approved.
    """
    # Strip leading/trailing whitespace and ensure command is not empty
    cmd = cmd.strip()
    if not cmd:
        raise ValueError("Empty command is not allowed.")

    # Safely split the command into arguments
    try:
        args = shlex.split(cmd)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    # Validate each subcommand against the approved list
    for token in args:
        if token not in approved_subcommands:
            raise ValueError(f"Disallowed subcommand detected: '{token}'")

    # Execute the command securely without invoking a shell
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=True  # Raise CalledProcessError on non-zero exit
        )
    except subprocess.CalledProcessError as exc:
        # Return the stderr if command fails
        return f"Command failed with exit code {exc.returncode}:\n{exc.stderr.strip()}"
    except FileNotFoundError:
        return f"Command not found: {args[0]}"

    # Return the standard output
    return result.stdout.strip()