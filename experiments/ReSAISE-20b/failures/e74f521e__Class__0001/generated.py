import subprocess
import shutil

def run_shell_cmd(cmd: str, params: list) -> str:
    """
    Execute a shell command with the provided arguments and return its output.

    Parameters
    ----------
    cmd : str
        The executable command to run.
    params : list
        A list of arguments for the command.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If the command cannot be found or fails to execute.
    """
    # Ensure the command exists on the system
    if shutil.which(cmd) is None:
        raise ValueError(f"Command not found: {cmd}")

    # Build the argument list for subprocess
    if not isinstance(params, list):
        raise ValueError("params must be a list of arguments")
    args = [cmd] + params

    try:
        # Execute the command without invoking a shell
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False,  # We will handle errors manually
        )
    except Exception as exc:
        raise ValueError(f"Failed to execute command '{cmd}': {exc}") from exc

    # If the process exited with a non-zero status, treat it as an error
    if result.returncode != 0:
        err_msg = (
            f"Command '{cmd}' failed with exit code {result.returncode}.\n"
            f"stderr: {result.stderr.strip()}"
        )
        raise ValueError(err_msg)

    return result.stdout