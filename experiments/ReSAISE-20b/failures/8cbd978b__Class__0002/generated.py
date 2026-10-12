import shlex
import subprocess
from typing import List


def filter_and_run_os_command(
    exec_command: str,
    whitelisted_subcommands: List[str]
) -> str:
    """
    Execute a shell command only if every token in the command is present
    in `whitelisted_subcommands`.  The function uses a safe tokenisation
    with shlex and runs the command via subprocess.run without a shell,
    mitigating CWE-77 (Command Injection).

    Parameters
    ----------
    exec_command : str
        The command string supplied by the caller.
    whitelisted_subcommands : list[str]
        A list of permitted subcommand tokens.  Each token in
        `exec_command` must appear in this list for the command to be executed.

    Returns
    -------
    str
        The decoded standard output if execution succeeds, otherwise an error
        message indicating the forbidden token.

    Raises
    ------
    ValueError
        If any subcommand token is not in `whitelisted_subcommands`.
    """
    # Tokenise the command safely
    try:
        tokens = shlex.split(exec_command)
    except ValueError as exc:  # pragma: no cover
        raise ValueError(f"Invalid command syntax: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command is not allowed")

    # Validate each token
    for token in tokens:
        if token not in whitelisted_subcommands:
            raise ValueError(f"Forbidden subcommand: {token!r}")

    # Execute the command safely (no shell)
    result = subprocess.run(
        tokens,
        capture_output=True,
        text=True,
        check=False
    )

    if result.returncode != 0:
        # Return stderr if the command failed
        return f"Command failed with exit code {result.returncode}:\n{result.stderr}"
    return result.stdout