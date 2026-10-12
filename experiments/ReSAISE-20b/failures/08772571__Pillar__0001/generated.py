import subprocess
import shlex
import shutil

def call_system_command(sys_command: str, params: list) -> str:
    """
    Execute a shell command with the supplied arguments and return its output.

    Parameters
    ----------
    sys_command : str
        The primary command to run.
    params : list
        A list of arguments for the command.

    Returns
    -------
    str
        The decoded standard output produced by the command.

    Raises
    ------
    ValueError
        If the command is not found or if execution fails.
    """
    # Ensure that the base command exists in the system PATH
    if not shutil.which(sys_command):
        raise ValueError(f"Command '{sys_command}' not found in PATH")

    # Build the argument list safely
    # `shlex.quote` is not needed here because we pass a list to subprocess.run,
    # but we use it to demonstrate safe tokenization of individual arguments
    # in case any argument contains shell metacharacters.
    args = [sys_command] + [shlex.quote(str(p)) for p in params]

    try:
        # Execute the command without invoking a shell
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False,          # We handle errors manually
            shell=False           # Prevent shell injection
        )
    except Exception as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command '{sys_command}' failed with exit code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout