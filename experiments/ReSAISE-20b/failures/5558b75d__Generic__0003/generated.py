import shlex
import subprocess
from typing import List

def filter_and_run_command(cmd_input: str, permitted_subcommands: List[str]) -> str:
    """
    Execute a shell command only if all its sub‑commands (tokens) are in the
    permitted_subcommands list.  Tokens that look like options (start with '-') are
    ignored from the permission check.

    Parameters
    ----------
    cmd_input : str
        The command line to be executed.
    permitted_subcommands : List[str]
        A list of allowed sub‑command tokens.

    Returns
    -------
    str
        The command's standard output if it ran successfully, or an error message
        explaining why the command was rejected.

    Raises
    ------
    ValueError
        If any token that is not an option is not in `permitted_subcommands`.
    """
    # Split the command safely
    try:
        tokens = shlex.split(cmd_input)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Empty command provided")

    # Validate each token
    for tok in tokens:
        if tok.startswith('-'):  # treat as an option flag
            continue
        if tok not in permitted_subcommands:
            raise ValueError(f"Command '{tok}' is not permitted")

    # Execute the command without invoking a shell
    result = subprocess.run(
        tokens,
        capture_output=True,
        text=True,
        check=False
    )

    if result.returncode != 0:
        return f"Command failed with exit code {result.returncode}:\n{result.stderr}"
    return result.stdout