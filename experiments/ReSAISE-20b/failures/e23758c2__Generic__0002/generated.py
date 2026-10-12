import os
import shlex
import subprocess
from typing import List

def validate_and_execute_command(input_command: str, permitted_subcommands: List[str]) -> str:
    """
    Execute a shell command only if every token in the command is present
    in *permitted_subcommands*.

    Parameters
    ----------
    input_command : str
        The command string supplied by the user.
    permitted_subcommands : list[str]
        A collection of tokens that are allowed to appear in the command.

    Returns
    -------
    str
        The combined stdout and stderr output from the executed command.

    Raises
    ------
    ValueError
        If the command is empty, or if any token in the command is not found
        in *permitted_subcommands*.
    RuntimeError
        If the subprocess call fails for any reason other than a non‑zero exit
        status (e.g., OSError).
    """
    if not input_command.strip():
        raise ValueError("Command cannot be empty.")

    # Safely split the command into tokens
    try:
        tokens = shlex.split(input_command)
    except ValueError as exc:  # pragma: no cover
        raise ValueError(f"Failed to parse command: {exc}") from exc

    # Validate each token
    for token in tokens:
        if token not in permitted_subcommands:
            raise ValueError(f"Token '{token}' is not permitted.")

    # Execute the command safely (no shell=True)
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False  # We'll handle non‑zero exit below
        )
    except OSError as exc:  # pragma: no cover
        raise RuntimeError(f"Execution failed: {exc}") from exc

    # Combine stdout and stderr for return
    output = result.stdout + result.stderr

    if result.returncode != 0:
        # You can decide whether to raise an exception or simply return the output.
        # Here we just return the output but you could uncomment the next line:
        # raise RuntimeError(f"Command exited with status {result.returncode}")
        pass

    return output