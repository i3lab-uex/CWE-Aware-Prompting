import shlex
import subprocess

def filter_and_run_command(cmd_input: str, permitted_subcommands: list) -> str:
    """
    Execute a shell command only if all subcommands are permitted.

    Parameters
    ----------
    cmd_input : str
        The command string supplied by the caller.
    permitted_subcommands : list[str]
        A list of subcommand names that are allowed.

    Returns
    -------
    str
        The standard output from the executed command, or an error message.

    Raises
    ------
    ValueError
        If the command is empty or any subcommand is not in the permitted list.
    """
    # Strip whitespace and ensure command is not empty
    cmd_input = cmd_input.strip()
    if not cmd_input:
        raise ValueError("Empty command is not allowed.")

    # Split the command safely using shlex
    try:
        parts = shlex.split(cmd_input)
    except ValueError as exc:
        raise ValueError(f"Failed to parse command: {exc}") from exc

    # Validate each subcommand against the permitted list
    for idx, part in enumerate(parts):
        if part not in permitted_subcommands:
            raise ValueError(
                f"Subcommand '{part}' at position {idx} is not permitted."
            )

    # Execute the command with shell=False to avoid injection
    try:
        result = subprocess.run(
            parts,
            capture_output=True,
            text=True,
            check=False,          # We'll handle errors manually
        )
    except OSError as exc:
        return f"Execution failed: {exc}"

    # Return stdout on success, otherwise include stderr
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return (
            f"Command failed with exit code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )