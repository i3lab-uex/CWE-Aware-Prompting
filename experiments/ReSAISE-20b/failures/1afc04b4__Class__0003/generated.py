import shlex
import subprocess

def run_shell_command_with_filters(command: str, allowed_subcommands_list: list) -> str:
    """
    Execute a shell command after validating that its first token (subcommand)
    is present in the allowed_subcommands_list.

    Parameters
    ----------
    command : str
        The shell command to execute.
    allowed_subcommands_list : list
        List of permitted subcommand names (e.g., ['ls', 'cat']).

    Returns
    -------
    str
        Standard output of the command if successful; otherwise, an error message.

    Raises
    ------
    ValueError
        If the command is empty, cannot be parsed, or its subcommand is not allowed.
    """
    if not command or not command.strip():
        raise ValueError("Command must not be empty")

    # Split the command safely; this will handle quoted arguments correctly.
    try:
        args = shlex.split(command)
    except ValueError as e:
        raise ValueError(f"Failed to parse command: {e}") from None

    if not args:
        raise ValueError("Command could not be parsed into arguments")

    # Validate the subcommand (first token)
    subcommand = args[0]
    if subcommand not in allowed_subcommands_list:
        raise ValueError(f"Disallowed subcommand: {subcommand}")

    # Execute the command without invoking a shell to avoid injection.
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False,          # We will handle errors manually
        )
    except FileNotFoundError:
        return f"Command not found: {subcommand}"
    except Exception as exc:
        return f"Execution failed: {exc}"

    # If the command exited with a non-zero status, return stderr.
    if result.returncode != 0:
        return f"Error ({result.returncode}): {result.stderr.strip()}"

    # Successful execution: return stdout.
    return result.stdout.strip()