import shlex
import subprocess
from typing import List


def filter_and_run_command(cmd_input: str, permitted_subcommands: List[str]) -> str:
    """
    Execute a shell command only if all subcommands are in the permitted list.

    Parameters
    ----------
    cmd_input : str
        The command string to be executed.
    permitted_subcommands : list[str]
        A list of subcommand names that are allowed to run.

    Returns
    -------
    str
        The stdout output of the command if it executes successfully,
        or an error message indicating that the command was not allowed.

    Raises
    ------
    ValueError
        If any subcommand in the input is not present in `permitted_subcommands`.
    """
    # Safely split the command into arguments
    try:
        args = shlex.split(cmd_input)
    except ValueError as exc:
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not args:
        raise ValueError("Empty command provided")

    # Check each subcommand against the permitted list
    for arg in args:
        if arg not in permitted_subcommands:
            raise ValueError(f"Command '{arg}' is not allowed")

    # Execute the command securely (no shell expansion)
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=True,          # raise CalledProcessError on non-zero exit
        )
    except subprocess.CalledProcessError as exc:
        # Return stderr if command fails but was permitted
        return f"Command failed with exit code {exc.returncode}:\n{exc.stderr}"
    except FileNotFoundError as exc:
        return f"Command not found: {exc}"

    return result.stdout