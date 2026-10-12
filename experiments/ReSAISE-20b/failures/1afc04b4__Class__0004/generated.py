import subprocess
import shlex

def run_shell_command_with_filters(command: str, allowed_subcommands_list: list[str]) -> str:
    """
    Execute a shell command after validating that the requested subcommand is in an
    allow‑list.  The function uses `subprocess.run` with `shell=False` to avoid
    shell injection vulnerabilities.

    Parameters
    ----------
    command : str
        The full shell‑style command to run.
    allowed_subcommands_list : list[str]
        A list of allowed subcommand names (the first token in the command).

    Returns
    -------
    str
        The decoded standard output of the command, or an error message.

    Raises
    ------
    ValueError
        If `command` is empty, or the first token does not appear in
        ``allowed_subcommands_list``.
    """
    if not command or not command.strip():
        raise ValueError("Command must not be empty")

    # Split the command into tokens safely
    try:
        tokens = shlex.split(command)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Command contains no executable part")

    subcommand = tokens[0]
    if subcommand not in allowed_subcommands_list:
        raise ValueError(f"Disallowed subcommand: {subcommand!r}")

    # Run the command safely without a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False,   # We'll handle non‑zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        return f"Command not found: {subcommand}"
    except Exception as exc:
        return f"Execution error: {exc}"

    if result.returncode != 0:
        # Include stderr in the returned message
        return f"Error ({result.returncode}): {result.stderr.strip()}"
    return result.stdout.strip()