import subprocess
import shlex

def run_shell_command(shell_command: str, parameters: list) -> str:
    """
    Execute a shell command with the given arguments and return its stdout output.

    Args:
        shell_command: The base command to run (e.g., 'ls', 'git').
        parameters: A list of string arguments to pass to the command.

    Returns:
        The decoded standard output from the executed command.

    Raises:
        ValueError: If the command cannot be found, fails to execute,
                    or returns a non‑zero exit status.
    """
    if not isinstance(shell_command, str):
        raise ValueError("shell_command must be a string")
    if not isinstance(parameters, list) or not all(isinstance(p, str) for p in parameters):
        raise ValueError("parameters must be a list of strings")

    # Build the argument list safely without using shell=True
    cmd = [shell_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,          # Decode stdout/stderr to str automatically
            check=False         # We'll handle non‑zero exit codes ourselves
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {shell_command}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command: {exc}") from exc

    if result.returncode != 0:
        # Include stderr in the error message for easier debugging
        raise ValueError(
            f"Command '{shell_command}' exited with code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )

    return result.stdout