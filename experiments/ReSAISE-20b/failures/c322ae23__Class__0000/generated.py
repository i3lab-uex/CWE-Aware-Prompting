import subprocess
import shlex


def run_command_with_args(base_command: str, parameters: list) -> str:
    """
    Execute an external command safely with the given arguments.

    Parameters
    ----------
    base_command : str
        The primary command to run.  It may be a simple executable name or a
        space‑separated string containing the command and its default arguments.
    parameters : list
        A list of additional arguments to pass to the command.  Each element is
        treated as a single argument and must not contain shell metacharacters.

    Returns
    -------
    str
        The combined stdout and stderr output of the executed command.

    Raises
    ------
    ValueError
        If the command cannot be executed or if it exits with a non‑zero status.
    """
    # Split the base command safely, preserving quoted groups
    try:
        cmd_parts = shlex.split(base_command)
    except ValueError as exc:
        raise ValueError(f"Invalid base command: {base_command}") from exc

    # Append user supplied parameters.  We rely on the caller to provide
    # properly escaped arguments; each item is passed as a literal string.
    cmd = cmd_parts + list(map(str, parameters))

    try:
        # Execute without invoking a shell to avoid command injection.
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,          # decode bytes to str using locale encoding
            check=False         # we handle non‑zero exit codes ourselves
        )
    except OSError as exc:
        raise ValueError(f"Execution failed for command: {' '.join(cmd)}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{' '.join(cmd)}' exited with status {result.returncode}:\n{result.stdout}"
        )

    return result.stdout