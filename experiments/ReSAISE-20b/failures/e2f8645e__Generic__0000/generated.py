import shlex
import subprocess
import os


def execute_command_with_restrictions(cmd: str, approved_subcommands: list) -> str:
    """
    Execute a shell command only if its primary subcommand is in the approved list.

    Parameters
    ----------
    cmd : str
        The command string to execute.
    approved_subcommands : list[str]
        A list of allowed primary subcommand names (e.g., ['ls', 'echo']).

    Returns
    -------
    str
        The stdout of the command if it executes successfully, or an error message.

    Raises
    ------
    ValueError
        If the command is empty or its primary subcommand is not approved.
    """
    # Strip leading/trailing whitespace
    cmd = cmd.strip()
    if not cmd:
        raise ValueError("No command provided.")

    # Split the command safely using shlex
    try:
        parts = shlex.split(cmd)
    except ValueError as exc:   # malformed quoting
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not parts:
        raise ValueError("Command contains no executable part.")

    # The first token is considered the primary subcommand
    primary = parts[0]

    if primary not in approved_subcommands:
        raise ValueError(f"Command '{primary}' is not allowed.")

    # Optional: ensure the executable exists in PATH
    if not shutil.which(primary):
        raise ValueError(f"Executable '{primary}' not found in PATH.")

    # Execute the command securely (no shell=True)
    try:
        result = subprocess.run(
            parts,
            capture_output=True,
            text=True,
            check=False,  # we handle non-zero exit codes ourselves
        )
    except OSError as exc:
        return f"Execution failed: {exc}"

    if result.returncode != 0:
        # Return stderr as the error message
        return f"Command failed (exit {result.returncode}): {result.stderr.strip()}"

    # Return stdout
    return result.stdout.strip()