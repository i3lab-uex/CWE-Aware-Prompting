import subprocess
import shlex
import shutil

def execute_shell_command(command: str, args: list) -> str:
    """
    Execute a shell command with the supplied arguments and return its output.

    Parameters
    ----------
    command : str
        The base command to execute. Must be a valid executable on the system.
    args : list
        A list of arguments to pass to the command. Elements are treated as literal
        arguments; no shell expansion or interpretation is performed.

    Returns
    -------
    str
        The combined stdout and stderr output of the command, decoded as UTF-8.

    Raises
    ------
    ValueError
        If the command is empty, not found, or if execution fails.
    """
    # Basic validation
    if not command:
        raise ValueError("Command must be a non-empty string")

    # Ensure the command is an executable on the system
    cmd_path = shutil.which(command)
    if not cmd_path:
        raise ValueError(f"Command '{command}' not found in PATH")

    # Construct the argument list safely
    if not isinstance(args, list):
        raise ValueError("Args must be a list")
    # Ensure each argument is string convertible
    safe_args = [str(a) for a in args]

    # Full command as list; no shell expansion
    full_cmd = [cmd_path] + safe_args

    try:
        result = subprocess.run(
            full_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
            text=True,  # decode as UTF-8 automatically
        )
    except subprocess.CalledProcessError as exc:
        # Include output in the error message for debugging
        raise ValueError(
            f"Command '{command}' failed with exit code {exc.returncode}:\n{exc.output}"
        ) from exc
    except OSError as exc:
        raise ValueError(f"Failed to execute command '{command}': {exc}") from exc

    return result.stdout