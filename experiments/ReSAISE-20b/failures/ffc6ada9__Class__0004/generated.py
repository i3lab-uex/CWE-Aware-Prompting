import subprocess
import shutil

def execute_command(base_command: str, parameters: list) -> str:
    """
    Execute a shell command safely with the given parameters.

    Parameters
    ----------
    base_command : str
        The main command to execute.
    parameters : list
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output of the executed command.

    Raises
    ------
    ValueError
        If the base_command is empty, not found in PATH,
        or if execution fails.
    """
    # Basic validation
    if not isinstance(base_command, str) or not base_command.strip():
        raise ValueError("base_command must be a non-empty string")

    if not isinstance(parameters, list):
        raise ValueError("parameters must be a list")

    # Ensure all parameters are strings
    for idx, p in enumerate(parameters):
        if not isinstance(p, str):
            raise ValueError(f"parameter at index {idx} is not a string")

    # Check that the command exists in PATH
    if shutil.which(base_command) is None:
        raise ValueError(f"command '{base_command}' not found in PATH")

    # Build the command list
    cmd = [base_command] + parameters

    try:
        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
    except subprocess.CalledProcessError as e:
        # Include the output in the error message for debugging
        raise ValueError(f"Command '{base_command}' failed with exit code {e.returncode}:\n{e.output}") from e
    except OSError as e:
        # Handle cases where the executable cannot be run
        raise ValueError(f"Execution failed: {e}") from e

    return result.stdout