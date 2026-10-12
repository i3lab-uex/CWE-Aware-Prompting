import subprocess
from typing import List

def run_command_with_args(base_command: str, parameters: List[str]) -> str:
    """
    Execute an external command with the provided arguments and return its output.

    Args:
        base_command (str): The primary command to run.
        parameters (List[str]): A list of arguments for the command.

    Returns:
        str: The standard output produced by the command.

    Raises:
        ValueError: If the command is invalid, fails to execute,
                    or if inputs are not properly formatted.
    """
    # Basic input validation
    if not isinstance(base_command, str) or not base_command.strip():
        raise ValueError("base_command must be a non-empty string")

    if not isinstance(parameters, list):
        raise ValueError("parameters must be a list of strings")

    for idx, arg in enumerate(parameters):
        if not isinstance(arg, str):
            raise ValueError(f"parameter at index {idx} is not a string")

    # Construct the command list without invoking the shell
    cmd = [base_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,          # Raise CalledProcessError on non-zero exit
        )
    except FileNotFoundError as e:
        raise ValueError(f"Command not found: {base_command}") from e
    except subprocess.CalledProcessError as e:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command '{base_command}' failed with exit code {e.returncode}.\n"
            f"Stdout: {e.stdout}\nStderr: {e.stderr}"
        ) from e
    except Exception as e:
        # Catch-all for unforeseen errors, but do not expose internals
        raise ValueError(f"Failed to execute command '{base_command}': {e}") from e

    # Return the trimmed stdout; any trailing newlines are removed
    return result.stdout.strip()