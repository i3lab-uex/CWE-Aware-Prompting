import shlex
import subprocess
from typing import List

def validate_and_execute_command(
    input_command: str,
    permitted_subcommands: List[str]
) -> str:
    """
    Execute a shell command only if every token in the command is present
    in ``permitted_subcommands``.

    Parameters
    ----------
    input_command : str
        The command string supplied by the caller.
    permitted_subcommands : list[str]
        A collection of strings that are considered safe to execute.

    Returns
    -------
    str
        The stdout of the executed command (decoded as UTF‑8).

    Raises
    ------
    ValueError
        If the command is empty, contains an unknown token,
        or if any token fails validation.
    RuntimeError
        If the underlying command returns a non‑zero exit status.
    """
    # Strip leading/trailing whitespace and ensure the command is not empty
    stripped = input_command.strip()
    if not stripped:
        raise ValueError("Empty command is not allowed")

    # Tokenise the command safely
    try:
        tokens = shlex.split(stripped)
    except ValueError as exc:   # malformed quoting, etc.
        raise ValueError(f"Command parsing failed: {exc}") from exc

    # Validate each token against the whitelist
    for tok in tokens:
        if tok not in permitted_subcommands:
            raise ValueError(f"Token '{tok}' is not permitted")

    # Execute the command safely using subprocess
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,          # returns strings instead of bytes
            check=False         # we handle non‑zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {exc}") from exc
    except Exception as exc:
        raise RuntimeError(f"Execution failed: {exc}") from exc

    if result.returncode != 0:
        raise RuntimeError(
            f"Command exited with {result.returncode}: "
            f"{result.stderr.strip()}"
        )

    return result.stdout