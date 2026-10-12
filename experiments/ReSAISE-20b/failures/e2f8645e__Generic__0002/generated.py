import os
import shlex
import subprocess

def execute_command_with_restrictions(cmd: str, approved_subcommands: list) -> str:
    """
    Execute a shell command only if all of its tokens are in the approved_subcommands list.
    
    Parameters
    ----------
    cmd : str
        The command string to be executed.
    approved_subcommands : list[str]
        A list of strings that are considered safe and allowed to appear in the command.
    
    Returns
    -------
    str
        The stdout of the successfully executed command.
    
    Raises
    ------
    ValueError
        If any token of the command is not present in `approved_subcommands`.
    """
    # Split the command safely into tokens
    try:
        tokens = shlex.split(cmd)
    except ValueError as exc:
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command provided")

    # Verify that every token is approved
    for token in tokens:
        if token not in approved_subcommands:
            raise ValueError(f"Command or subcommand '{token}' is not allowed")

    # Execute the command with shell=False to avoid shell injection
    result = subprocess.run(
        tokens,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=os.getcwd()
    )

    return result.stdout