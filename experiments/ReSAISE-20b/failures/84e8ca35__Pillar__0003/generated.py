import shlex
import subprocess
from typing import List


def restricted_command_executor(
    user_command: str,
    whitelist_commands: List[str],
) -> str:
    """
    Execute a user supplied command only if all tokens are in the whitelist.

    Parameters
    ----------
    user_command : str
        The shell command entered by the user.
    whitelist_commands : List[str]
        A list of permitted subcommands (e.g., ['ls', 'echo', 'cat']).

    Returns
    -------
    str
        The combined stdout and stderr of the executed command.

    Raises
    ------
    ValueError
        If any token in ``user_command`` is not present in ``whitelist_commands``.
    RuntimeError
        If the command fails to execute (e.g., missing executable).
    """
    # Split the user command into tokens in a shell‑safe manner
    try:
        tokens = shlex.split(user_command)
    except ValueError as exc:  # malformed quoting, etc.
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command is not allowed.")

    # Validate each token against the whitelist
    for token in tokens:
        if token not in whitelist_commands:
            raise ValueError(
                f"Command '{token}' is not permitted. "
                "Allowed commands: "
                + ", ".join(whitelist_commands)
            )

    # Execute the command securely (no shell expansion)
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,  # we will handle non‑zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        raise RuntimeError(f"Executable not found: {exc}") from exc
    except Exception as exc:
        raise RuntimeError(f"Failed to execute command: {exc}") from exc

    # Combine stdout and stderr for a single string return value
    output = result.stdout + result.stderr

    if result.returncode != 0:
        # Optionally, we could raise an error or simply return the output.
        # Here we include the exit status in the message for clarity.
        output += f"\nCommand exited with status {result.returncode}."

    return output