import shlex
import subprocess

def run_shell_command_with_filters(command: str, allowed_subcommands_list: list) -> str:
    """
    Execute a shell command after validating that every subcommand
    (i.e., each argument except the first) is present in the allowed list.

    Parameters
    ----------
    command : str
        The shell command to execute.
    allowed_subcommands_list : list
        A list of subcommand strings that are permitted.

    Returns
    -------
    str
        The standard output of the command if it succeeds, otherwise an error message.

    Raises
    ------
    ValueError
        If the command contains any subcommand not in ``allowed_subcommands_list``.
    """
    # Split the command safely
    try:
        parts = shlex.split(command)
    except ValueError as e:
        raise ValueError(f"Failed to parse command: {e}")

    if not parts:
        raise ValueError("Empty command provided")

    # Validate each subcommand (skip the main executable)
    disallowed = [p for p in parts[1:] if p not in allowed_subcommands_list]
    if disallowed:
        raise ValueError(f"Disallowed subcommand(s) detected: {', '.join(disallowed)}")

    # Execute the command
    try:
        result = subprocess.run(
            parts,
            capture_output=True,
            text=True,
            check=False,  # We handle non-zero exit codes ourselves
        )
    except FileNotFoundError:
        return f"Command not found: {parts[0]}"
    except Exception as exc:
        return f"Error executing command: {exc}"

    # Build the output string
    if result.returncode != 0:
        return (
            f"Command exited with code {result.returncode}\n"
            f"Stdout:\n{result.stdout}\nStderr:\n{result.stderr}"
        )
    return result.stdout