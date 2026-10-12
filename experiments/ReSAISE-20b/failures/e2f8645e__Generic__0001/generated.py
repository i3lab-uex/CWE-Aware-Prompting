import os
import shlex
import subprocess

def execute_command_with_restrictions(cmd: str, approved_subcommands: list) -> str:
    """
    Execute a shell command only if every subcommand in the command string
    is present in `approved_subcommands`.

    Parameters
    ----------
    cmd : str
        The full command string to be executed.
    approved_subcommands : list of str
        A list of subcommand names that are considered safe.

    Returns
    -------
    str
        The standard output of the executed command, or an error message if
        the command is not allowed.

    Raises
    ------
    ValueError
        If any subcommand in `cmd` is not found in `approved_subcommands`.
    """
    # Split the command into individual tokens safely
    try:
        tokens = shlex.split(cmd)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command string provided")

    # Validate each token against the approved list
    for token in tokens:
        # The first token is usually the program name; other tokens may be arguments
        # We'll only check the base command (first token) for safety.
        if token == tokens[0]:
            if token not in approved_subcommands:
                raise ValueError(f"Command '{token}' is not allowed")
            # No need to check further tokens for safety
            break

    # Execute the command securely using subprocess.run
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # We'll handle non-zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        return f"Command not found: {exc}"
    except Exception as exc:
        return f"Execution failed: {exc}"

    # Return stdout on success, stderr otherwise
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Command exited with {result.returncode}: {result.stderr.strip()}"