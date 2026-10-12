import subprocess
import shlex
import shutil

def execute_command(cmd: str, arguments: list) -> str:
    """
    Execute a shell command with the supplied arguments and return its output.

    Parameters
    ----------
    cmd : str
        The command to run (e.g., "ls", "grep").
    arguments : list
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output of the executed command.

    Raises
    ------
    ValueError
        If the command is not found or execution fails.
    """
    # Ensure the command exists in PATH
    if shutil.which(cmd) is None:
        raise ValueError(f"Command not found: {cmd}")

    # Build the full argument list
    cmd_list = [cmd] + [str(arg) for arg in arguments]

    try:
        # Run the command without invoking a shell to avoid injection
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            check=False,  # we handle non-zero exit codes ourselves
        )
    except Exception as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{cmd}' failed with exit code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout