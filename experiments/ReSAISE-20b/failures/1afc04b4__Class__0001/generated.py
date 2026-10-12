import shlex
import subprocess
from typing import List

def run_shell_command_with_filters(command: str, allowed_subcommands_list: List[str]) -> str:
    """
    Execute a shell command after validating that its first subcommand is in the
    allowed list. The function uses shlex to safely parse the command string
    and subprocess.run with shell=False to avoid shell injection.

    Parameters
    ----------
    command : str
        The full shell command to execute.
    allowed_subcommands_list : list[str]
        A list of subcommand names that are permitted.

    Returns
    -------
    str
        The standard output from the executed command, or an error message.

    Raises
    ------
    ValueError
        If the command is empty, malformed, or contains a disallowed subcommand.
    """
    # Strip whitespace and ensure the command is not empty
    cmd = command.strip()
    if not cmd:
        raise ValueError("Empty command provided")

    # Safely split the command into tokens
    try:
        args = shlex.split(cmd, posix=True)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not args:
        raise ValueError("Command contains no executable")

    # Validate the first token against allowed subcommands
    if args[0] not in allowed_subcommands_list:
        raise ValueError(f"Disallowed subcommand: {args[0]}")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False,          # We'll handle non-zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Executable not found: {args[0]}") from exc
    except Exception as exc:
        raise ValueError(f"Execution failed: {exc}") from exc

    # Return stdout or stderr based on exit status
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        # Include stderr for debugging; could also raise an exception
        return f"Command failed with exit code {result.returncode}:\n{result.stderr.strip()}"