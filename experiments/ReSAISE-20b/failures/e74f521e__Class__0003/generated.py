import subprocess
from shutil import which

def run_shell_cmd(cmd: str, params: list[str]) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    cmd : str
        The command to execute (must be an executable in the system PATH).
    params : list[str]
        A list of arguments to pass to the command.

    Returns
    -------
    str
        The decoded standard output of the executed command.

    Raises
    ------
    ValueError
        If the command cannot be found, is not executable,
        or if the subprocess fails to run.
    """
    # Basic validation
    if not isinstance(cmd, str) or not cmd.strip():
        raise ValueError("Command must be a non-empty string")
    if not isinstance(params, list) or not all(isinstance(p, str) for p in params):
        raise ValueError("Params must be a list of strings")

    # Ensure the command exists in PATH
    if which(cmd) is None:
        raise ValueError(f"Command '{cmd}' not found in PATH")

    # Build the argument list: [command, arg1, arg2, ...]
    full_cmd = [cmd] + params

    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,          # decode bytes to str
            check=True,         # raise CalledProcessError on non-zero exit
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command '{cmd}' not found") from exc
    except subprocess.CalledProcessError as exc:
        # Include stderr in the error message for debugging
        raise ValueError(
            f"Command '{cmd}' failed with exit code {exc.returncode}: "
            f"{exc.stderr.strip()}"
        ) from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command '{cmd}': {exc}") from exc

    return result.stdout.strip()