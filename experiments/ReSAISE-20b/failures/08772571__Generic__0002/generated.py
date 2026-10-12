import subprocess
import shlex

def call_system_command(sys_command: str, params: list) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Args:
        sys_command: The base command to run (may contain spaces).
        params: A list of string arguments for the command.

    Returns:
        The standard output produced by the command as a string.

    Raises:
        ValueError: If the command is invalid, fails to execute,
                    or returns a non-zero exit status.
    """
    if not isinstance(sys_command, str):
        raise ValueError("sys_command must be a string")
    if not isinstance(params, list) or not all(isinstance(p, str) for p in params):
        raise ValueError("params must be a list of strings")

    # Safely split the base command and combine with arguments
    try:
        cmd_list = shlex.split(sys_command) + params
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to parse command: {exc}") from exc

    try:
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            check=False  # We handle errors manually
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {sys_command}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        raise ValueError(
            f"Command '{' '.join(cmd_list)}' failed with exit code {result.returncode}:\n{result.stderr}"
        )

    return result.stdout