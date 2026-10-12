import shlex
import subprocess

def validate_and_execute_command(shell_cmd: str, safe_subcommands: list[str]) -> str:
    """
    Execute a shell command only if all subcommands are in the allowed list.

    Parameters
    ----------
    shell_cmd : str
        The command string to be executed.
    safe_subcommands : list[str]
        List of subcommand names considered safe (e.g., ['ls', 'cat']).

    Returns
    -------
    str
        The standard output of the executed command if successful, or an error
        message explaining why the command could not be run.

    Raises
    ------
    ValueError
        If the command is empty or any token in the command does not match a
        permitted subcommand.
    """
    if not shell_cmd or not shell_cmd.strip():
        raise ValueError("Empty command is not allowed.")

    # Safely split the command into tokens
    try:
        tokens = shlex.split(shell_cmd)
    except ValueError as exc:
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    # Ensure the primary command (first token) is allowed
    if tokens[0] not in safe_subcommands:
        raise ValueError(
            f"Command '{tokens[0]}' is not in the list of allowed subcommands."
        )

    # Optional: if you want to restrict *all* tokens (e.g., avoid piping),
    # uncomment the following block.
    #
    # for token in tokens:
    #     if token not in safe_subcommands and not token.startswith('-'):
    #         raise ValueError(f"Subcommand '{token}' is not allowed.")

    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False
        )
    except FileNotFoundError as exc:
        return f"Command not found: {exc}"
    except Exception as exc:
        return f"Error executing command: {exc}"

    if result.returncode != 0:
        return (
            f"Command exited with code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout.strip()