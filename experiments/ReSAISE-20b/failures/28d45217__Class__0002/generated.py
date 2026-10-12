import shlex
import subprocess

def validate_and_execute_command(input_command: str, permitted_subcommands: list) -> str:
    """
    Execute a shell command only if all tokens are in the permitted_subcommands list.

    Parameters
    ----------
    input_command : str
        The raw command string supplied by the user.
    permitted_subcommands : list[str]
        A collection of strings that are allowed to appear in the command.

    Returns
    -------
    str
        The stdout of the executed command, or an error message if execution is forbidden.

    Raises
    ------
    ValueError
        If any token in the command is not present in `permitted_subcommands`.
    """
    # Tokenise safely; this will handle quoted strings correctly
    try:
        tokens = shlex.split(input_command, posix=True)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command is not allowed.")

    # Verify each token against the permitted list
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Forbidden subcommand or argument: '{token}'")

    # Execute the command securely without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,   # we will handle non‑zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        return f"Command not found: {tokens[0]}"
    except Exception as exc:
        return f"Execution failed: {exc}"

    # Return stdout or stderr depending on exit status
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Command exited with {result.returncode}:\n{result.stderr.strip()}"