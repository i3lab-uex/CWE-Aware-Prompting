import shlex
import subprocess
from typing import List


def filter_and_run_os_command(exec_command: str, whitelisted_subcommands: List[str]) -> str:
    """
    Execute a shell command only if it is in the list of whitelisted subcommands.

    Parameters
    ----------
    exec_command : str
        The command string requested by the user.
    whitelisted_subcommands : List[str]
        A list of permitted command names (e.g., ['ls', 'echo']).

    Returns
    -------
    str
        The stdout of the executed command, or an error message if execution fails.

    Raises
    ------
    ValueError
        If the command is empty, contains disallowed subcommands,
        or the first token is not in the whitelist.
    """
    # Strip whitespace and ensure something was provided
    stripped = exec_command.strip()
    if not stripped:
        raise ValueError("No command provided.")

    # Safely split the command into arguments
    try:
        args = shlex.split(stripped)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    # Basic check: first token (the program name) must be whitelisted
    cmd_name = args[0]
    if cmd_name not in whitelisted_subcommands:
        raise ValueError(f"Command '{cmd_name}' is not allowed.")

    # Optional: ensure no other subcommands or dangerous tokens are present
    # (e.g., no pipes, redirects, etc.). Since we use shell=False,
    # these are not interpreted by the shell anyway.

    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False,      # We handle non-zero exit codes ourselves
            shell=False       # Avoid shell interpretation to mitigate injection
        )
    except FileNotFoundError:
        raise ValueError(f"Executable '{cmd_name}' not found.")
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        # Return the stderr as part of the error message
        return f"Command failed with exit code {result.returncode}:\n{result.stderr.strip()}"
    return result.stdout.strip()