import subprocess
import shlex
import shutil
from typing import List

def run_shell_command(shell_command: str, parameters: List[str]) -> str:
    """
    Execute a shell command with the supplied arguments and return its stdout.

    Parameters
    ----------
    shell_command : str
        The command to run (e.g. "ls", "grep").
    parameters : List[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output of the command.

    Raises
    ------
    ValueError
        If the command cannot be found, or execution fails.
    """
    # Ensure the base command is a valid executable
    cmd_path = shutil.which(shell_command)
    if not cmd_path:
        raise ValueError(f"Command '{shell_command}' not found in PATH.")

    # Split the base command to handle any embedded quoting (rare but safe)
    base_parts = shlex.split(shell_command, posix=True)

    # Construct the full argument list: base command + parameters
    full_cmd = base_parts + parameters

    try:
        # Run the process without invoking a shell to avoid injection issues
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,          # decode bytes to str using locale encoding
            check=True,         # raise CalledProcessError on non-zero exit
        )
    except subprocess.CalledProcessError as exc:
        # Wrap the original error in a ValueError with context
        raise ValueError(
            f"Command '{' '.join(full_cmd)}' failed with exit code {exc.returncode}.\n"
            f"stderr: {exc.stderr.strip()}"
        ) from exc
    except OSError as exc:
        # Handle issues like permission denied, file not found, etc.
        raise ValueError(f"Execution failed: {exc}") from exc

    return result.stdout