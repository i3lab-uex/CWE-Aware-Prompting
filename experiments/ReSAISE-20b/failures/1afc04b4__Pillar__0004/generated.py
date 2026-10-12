import shlex
import subprocess


def run_shell_command_with_filters(command: str, allowed_subcommands_list):
    """
    Execute a shell command after ensuring that its subcommand is in the allowed list.

    Parameters
    ----------
    command : str
        The shell command to execute (e.g. "git commit -m 'msg'").
    allowed_subcommands_list : list
        A list of subcommand names that are permitted (e.g. ["commit", "push"]).

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command is empty, cannot be parsed, or contains a disallowed subcommand.
    RuntimeError
        If the command fails to execute (non‑zero exit status).
    """
    if not isinstance(command, str) or not command.strip():
        raise ValueError("Command must be a non‑empty string.")

    # Safely split the command into tokens without invoking a shell
    try:
        tokens = shlex.split(command)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Command contains no executable tokens.")

    # The first token is the program; the second (if present) is treated as a subcommand.
    # This simple rule works for commands like "git commit" or "svn update".
    subcommand = tokens[1] if len(tokens) > 1 else None

    # Validate the subcommand
    if subcommand and subcommand not in allowed_subcommands_list:
        raise ValueError(f"Disallowed subcommand: '{subcommand}'")

    # Execute the command without using a shell to avoid injection attacks.
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # We handle non‑zero exit codes ourselves
        )
    except OSError as exc:
        raise RuntimeError(f"Execution failed: {exc}") from exc

    if result.returncode != 0:
        # Include stderr in the error message for easier debugging
        raise RuntimeError(
            f"Command failed with exit code {result.returncode}:\n{result.stderr}"
        )

    return result.stdout