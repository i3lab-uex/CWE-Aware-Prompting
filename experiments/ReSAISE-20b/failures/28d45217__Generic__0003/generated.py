import shlex
import subprocess
from typing import List


def validate_and_execute_command(
    input_command: str, permitted_subcommands: List[str]
) -> str:
    """
    Execute a shell command only if all of its subcommands are permitted.

    Parameters
    ----------
    input_command : str
        The command string to be executed.
    permitted_subcommands : list[str]
        A collection of allowed subcommand tokens.

    Returns
    -------
    str
        The combined stdout and stderr from the executed command if it is allowed.

    Raises
    ------
    ValueError
        If any token in the command is not present in ``permitted_subcommands``.
    """
    # Split the input safely into tokens
    try:
        tokens = shlex.split(input_command)
    except ValueError as exc:
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command")

    # Validate every token against the allowed list
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(
                f"Forbidden subcommand: '{token}'. Allowed subcommands are: "
                f"{', '.join(permitted_subcommands)}"
            )

    # Execute the command safely using subprocess
    result = subprocess.run(
        tokens,
        capture_output=True,
        text=True,
        shell=False,  # do not use the shell to avoid injection
    )

    output = result.stdout + result.stderr
    return output.strip()