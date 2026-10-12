import shlex
import subprocess

def run_shell_command_with_filters(command: str, allowed_subcommands_list: list) -> str:
    """
    Execute a shell command after filtering its tokens against an allowed set.

    Parameters
    ----------
    command : str
        The shell command to execute.
    allowed_subcommands_list : list[str]
        List of subcommand tokens that are permitted.

    Returns
    -------
    str
        The standard output from the command, or an error message.

    Raises
    ------
    ValueError
        If `command` is empty, contains disallowed tokens,
        or if any token fails to be recognized as allowed.
    """
    # Basic sanity checks
    if not isinstance(command, str) or not command.strip():
        raise ValueError("Command must be a non‑empty string.")

    if not isinstance(allowed_subcommands_list, list) or not all(
        isinstance(x, str) for x in allowed_subcommands_list
    ):
        raise ValueError("allowed_subcommands_list must be a list of strings.")

    # Split the command safely into tokens
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    if not tokens:
        raise ValueError("Command contains no executable token.")

    # Validate each token against the allowed list
    for token in tokens:
        if token not in allowed_subcommands_list:
            raise ValueError(
                f"Disallowed subcommand detected: '{token}'. "
                "Execution aborted."
            )

    # Execute the command without invoking a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,  # automatically decode bytes to str
            check=False,  # we handle non‑zero exit codes ourselves
        )
    except Exception as exc:
        return f"Execution failed: {exc}"

    # Return stdout or stderr depending on exit status
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        # Provide both stdout and stderr for debugging
        err_msg = result.stderr.strip()
        out_msg = result.stdout.strip()
        return (
            f"Command exited with code {result.returncode}.\n"
            f"STDOUT:\n{out_msg}\n"
            f"STDERR:\n{err_msg}"
        )