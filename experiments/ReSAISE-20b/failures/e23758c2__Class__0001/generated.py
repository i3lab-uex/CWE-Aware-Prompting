import shlex
import subprocess
from typing import List


def validate_and_execute_command(
    input_command: str,
    permitted_subcommands: List[str]
) -> str:
    """
    Execute a shell command only if all its subcommands are in the
    permitted_subcommands list.

    Parameters
    ----------
    input_command : str
        The command string supplied by the user.
    permitted_subcommands : list[str]
        A collection of allowed subcommand tokens.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If any token in the parsed command is not in `permitted_subcommands`.
    """
    # Tokenise the input safely
    try:
        tokens = shlex.split(input_command)
    except ValueError as exc:          # pragma: no cover
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command is not allowed")

    # Validate each token against the whitelist
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Unauthorized subcommand: {token!r}")

    # Execute the command safely (no shell expansion)
    result = subprocess.run(
        tokens,
        capture_output=True,
        text=True,
        check=False
    )

    # Raise an exception if the command failed (non‑zero exit code)
    if result.returncode != 0:
        raise ValueError(
            f"Command failed with exit code {result.returncode}: "
            f"{result.stderr.strip()}"
        )

    return result.stdout