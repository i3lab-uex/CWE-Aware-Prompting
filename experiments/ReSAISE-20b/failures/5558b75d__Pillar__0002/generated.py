import os
import shlex
import subprocess

def filter_and_run_command(cmd_input: str, permitted_subcommands: list) -> str:
    """
    Execute a shell command only if all tokens are in the permitted_subcommands list.
    
    Parameters
    ----------
    cmd_input : str
        The command string supplied by the caller.
    permitted_subcommands : list
        A list of tokens that are considered safe. The command will be executed only if every token
        in the parsed command is present in this list.

    Returns
    -------
    str
        The standard output of the executed command, decoded as UTF-8.

    Raises
    ------
    ValueError
        If the command is empty, contains disallowed tokens, or if execution fails.
    """
    # Strip whitespace and ensure we have something to run
    cmd_input = cmd_input.strip()
    if not cmd_input:
        raise ValueError("Empty command is not allowed.")

    # Safely split the input into tokens
    try:
        cmd_tokens = shlex.split(cmd_input, posix=True)
    except ValueError as e:
        raise ValueError(f"Failed to parse command: {e}")

    # Ensure every token is permitted
    for token in cmd_tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Disallowed subcommand or argument: '{token}'")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            cmd_tokens,
            capture_output=True,
            text=True,  # Decodes stdout/stderr to str
            check=False,  # We'll handle errors ourselves
        )
    except OSError as e:
        raise ValueError(f"Execution failed: {e}")

    # Return stdout if the command succeeded, otherwise an error message
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        error_msg = (
            f"Command failed with exit code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )
        raise ValueError(error_msg)