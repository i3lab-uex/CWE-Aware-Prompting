import os
import shlex
import subprocess

def validate_and_execute_command(shell_cmd: str, safe_subcommands: list) -> str:
    """
    Execute a shell command only if all its subcommands are in the safe_subcommands list.

    Parameters
    ----------
    shell_cmd : str
        The command string to be executed.
    safe_subcommands : list
        List of allowed subcommand names (e.g., ['ls', 'echo']).

    Returns
    -------
    str
        Standard output of the command if executed successfully.

    Raises
    ------
    ValueError
        If any subcommand is not in safe_subcommands or if the command fails.
    """
    # Split the command into tokens safely
    try:
        cmd_tokens = shlex.split(shell_cmd)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not cmd_tokens:
        raise ValueError("Empty command provided")

    # Validate each subcommand against the safe list
    for token in cmd_tokens:
        if token not in safe_subcommands:
            raise ValueError(f"Command '{token}' is not allowed")

    # Execute the command securely
    try:
        result = subprocess.run(
            cmd_tokens,
            capture_output=True,
            text=True,
            check=True,          # Raise CalledProcessError on non-zero exit
        )
    except subprocess.CalledProcessError as exc:
        # Return the stderr as part of the error message
        raise ValueError(
            f"Command execution failed with exit code {exc.returncode}: "
            f"{exc.stderr.strip()}"
        ) from exc
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {exc}") from exc

    return result.stdout.strip()