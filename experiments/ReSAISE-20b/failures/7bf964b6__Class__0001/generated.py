import os
import shlex
import subprocess

def validate_and_execute_command(shell_cmd: str, safe_subcommands: list) -> str:
    """
    Execute a shell command only if all its sub‑components are allowed.

    Parameters
    ----------
    shell_cmd : str
        The full command string to run.
    safe_subcommands : list
        A list of strings that are considered safe and permitted as sub‑commands.
        The first token (the executable) is not validated against this list.

    Returns
    -------
    str
        The standard output of the command if it succeeds, otherwise an error message.

    Raises
    ------
    ValueError
        If the command is empty, or any of its sub‑components (excluding the executable)
        are not present in ``safe_subcommands``.
    """
    if not shell_cmd.strip():
        raise ValueError("Empty command is not allowed.")

    # Safely split the command into tokens, respecting quoting.
    try:
        args = shlex.split(shell_cmd)
    except ValueError as e:
        raise ValueError(f"Failed to parse command: {e}")

    if not args:
        raise ValueError("No executable found in the command.")

    # Validate each sub‑command (excluding the executable itself).
    for token in args[1:]:
        if token not in safe_subcommands:
            raise ValueError(
                f"Disallowed sub‑command detected: '{token}'. "
                "Only the following are permitted: "
                f"{', '.join(safe_subcommands)}"
            )

    # Execute the command safely without invoking a shell.
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False,      # We'll handle non‑zero exit codes ourselves.
        )
    except FileNotFoundError:
        return f"Executable not found: {args[0]}"
    except Exception as exc:
        return f"Execution failed: {exc}"

    # Return stdout or an error message if the command failed.
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        error_msg = (
            f"Command exited with status {result.returncode}.\n"
            f"stderr: {result.stderr.strip()}"
        )
        return error_msg