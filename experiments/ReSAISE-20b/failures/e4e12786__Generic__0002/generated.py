import subprocess
import shutil

def execute_shell_command(command: str, args: list[str]) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    command : str
        The base command to execute.
    args : list[str]
        A list of arguments for the command.

    Returns
    -------
    str
        The decoded stdout from the executed command.

    Raises
    ------
    ValueError
        If the command cannot be found or execution fails.
    """
    # Ensure the base command exists on the system
    if not shutil.which(command):
        raise ValueError(f"Command '{command}' not found or is not executable.")

    # Build the full command list
    cmd = [command] + args

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,          # decode bytes to str automatically
            check=True          # raise CalledProcessError on non-zero exit
        )
    except subprocess.CalledProcessError as exc:
        # Provide a helpful error message
        raise ValueError(
            f"Command '{command}' failed with exit code {exc.returncode}.\n"
            f"Stdout: {exc.stdout}\nStderr: {exc.stderr}"
        ) from exc
    except OSError as exc:
        # Handles cases like permission denied, etc.
        raise ValueError(f"Failed to execute command '{command}': {exc}") from exc

    return result.stdout