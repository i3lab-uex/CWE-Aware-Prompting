import os
import shlex
import subprocess

def filter_and_run_command(cmd_input: str, permitted_subcommands: list) -> str:
    """
    Execute a shell command only if it passes through specific filters.

    Parameters
    ----------
    cmd_input : str
        The command to execute.
    permitted_subcommands : list
        A list of subcommands that are considered safe and permitted.

    Returns
    -------
    str
        The stdout of the successful command, or an error message if the
        command was not allowed.

    Raises
    ------
    ValueError
        If any part of the command does not match the allowed list.
    """
    # Split the input safely using shlex
    try:
        tokens = shlex.split(cmd_input)
    except ValueError as exc:  # malformed command
        raise ValueError(f"Malformed command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command")

    # Convert permitted list to a set for O(1) lookups
    allowed = set(permitted_subcommands)

    # Validate each token (command and sub‑arguments)
    for token in tokens:
        if token not in allowed:
            raise ValueError(f"Command or subcommand '{token}' is not permitted")

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # we handle errors manually
        )
    except OSError as exc:
        return f"Execution failed: {exc}"

    if result.returncode != 0:
        return (
            f"Command failed with exit code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout.strip()