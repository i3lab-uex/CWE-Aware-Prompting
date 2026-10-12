import subprocess
import shlex

def run_shell_command(cmd: str, arguments: list) -> str:
    """
    Execute a shell command with the given arguments and return its output.

    Parameters
    ----------
    cmd : str
        The base command to run (e.g., "ls", "echo").
    arguments : list
        A list of strings representing the command's arguments.

    Returns
    -------
    str
        The standard output produced by the command.

    Raises
    ------
    ValueError
        If `cmd` is empty, if the command fails to execute,
        or if the process exits with a non-zero return code.
    """
    # Basic validation
    if not isinstance(cmd, str) or not cmd.strip():
        raise ValueError("The command must be a non-empty string.")

    if not isinstance(arguments, list):
        raise ValueError("Arguments must be provided as a list.")

    # Construct the command line safely
    cmd_list = [cmd] + arguments

    try:
        # Execute the command.  Capture both stdout and stderr.
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            check=True,  # Raises CalledProcessError on non-zero exit
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Command not found: {cmd}") from exc
    except subprocess.CalledProcessError as exc:
        # Provide useful debugging information in the error message
        raise ValueError(
            f"Command '{shlex.join(cmd_list)}' failed with exit code {exc.returncode}.\n"
            f"Stdout: {exc.stdout}\nStderr: {exc.stderr}"
        ) from exc
    except Exception as exc:
        raise ValueError(f"Failed to execute command '{cmd}': {exc}") from exc

    return result.stdout