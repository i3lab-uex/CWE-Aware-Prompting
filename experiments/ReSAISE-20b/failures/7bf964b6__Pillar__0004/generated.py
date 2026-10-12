import os
import shlex
import subprocess

def validate_and_execute_command(shell_cmd: str, safe_subcommands: list) -> str:
    """
    Execute a shell command only if all subcommands are in the safe_subcommands list.

    Parameters
    ----------
    shell_cmd : str
        The command string to be executed.
    safe_subcommands : list[str]
        A list of subcommand names that are allowed to run.

    Returns
    -------
    str
        The standard output of the command if it executed successfully, or an error message
        explaining why execution was blocked.

    Raises
    ------
    ValueError
        If the command or any of its subcommands are not in the allowed list.
    """
    # Split the command safely
    try:
        parts = shlex.split(shell_cmd)
    except ValueError as exc:
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not parts:
        raise ValueError("Empty command is not allowed")

    # Validate each subcommand
    for part in parts:
        if part not in safe_subcommands:
            raise ValueError(f"Subcommand '{part}' is not allowed")

    # Execute the command securely
    try:
        result = subprocess.run(
            parts,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        # Return the stderr output as part of the error message
        return f"Command failed: {exc.stderr.strip()}"
    except OSError as exc:
        # Handle OS-level errors (e.g., command not found)
        return f"OS error: {exc.strerror}"

    # Return the captured stdout
    return result.stdout.strip()