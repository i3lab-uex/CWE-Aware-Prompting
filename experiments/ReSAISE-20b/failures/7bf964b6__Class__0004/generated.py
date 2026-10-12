import shlex
import subprocess

def validate_and_execute_command(shell_cmd: str, safe_subcommands: list[str]) -> str:
    """
    Execute a shell command only if every token in the command is present
    in the list of permitted subcommands.

    Parameters
    ----------
    shell_cmd : str
        The command to execute.
    safe_subcommands : list[str]
        A list of tokens that are considered safe and permitted.

    Returns
    -------
    str
        The standard output of the executed command, or an error message if the
        command was not allowed.

    Raises
    ------
    ValueError
        If any token in the command is not present in `safe_subcommands`.
    RuntimeError
        If the command execution fails for reasons other than a disallowed token.
    """
    # Split the command safely into tokens
    try:
        tokens = shlex.split(shell_cmd)
    except ValueError as exc:  # malformed shell syntax
        raise RuntimeError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command is not allowed.")

    # Ensure every token is in the safe list
    disallowed = [t for t in tokens if t not in safe_subcommands]
    if disallowed:
        raise ValueError(
            f"Command contains disallowed token(s): {', '.join(disallowed)}"
        )

    # Execute the command without invoking a shell to avoid injection
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as exc:
        # The command ran but failed (non-zero exit status)
        raise RuntimeError(
            f"Command execution failed: {exc.stderr.strip() or exc}"
        ) from exc
    except FileNotFoundError as exc:
        # The command itself was not found
        raise RuntimeError(f"Command not found: {exc}") from exc

    return result.stdout.strip()