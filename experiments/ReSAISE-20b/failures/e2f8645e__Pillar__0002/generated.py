import os
import shlex
import subprocess

def execute_command_with_restrictions(cmd: str, approved_subcommands: list[str]) -> str:
    """
    Execute a shell command only if it passes through specific filters.
    
    Parameters
    ----------
    cmd : str
        The command to execute. It should be a string that can be split into tokens.
    approved_subcommands : list[str]
        A list of subcommand names that are considered safe and permitted.  
        The first token (the program itself) is automatically allowed.
    
    Returns
    -------
    str
        The standard output of the command if executed successfully.
    
    Raises
    ------
    ValueError
        If the command or any of its subcommands are not in the approved list.
    """
    # Split the command safely into tokens
    try:
        tokens = shlex.split(cmd, posix=True)
    except ValueError as exc:  # malformed command line
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command provided")

    # The first token (program) is always allowed; check the rest
    for subcmd in tokens[1:]:
        if subcmd not in approved_subcommands:
            raise ValueError(f"Disallowed subcommand detected: {subcmd}")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {tokens[0]}") from exc

    # Return stdout if successful, otherwise return stderr as an error message
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        # Return stderr to provide feedback
        return result.stderr.strip() or f"Command exited with status {result.returncode}"