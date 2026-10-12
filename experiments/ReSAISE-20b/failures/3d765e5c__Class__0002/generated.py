import os
import shlex
import subprocess

def filtered_system_command(cmd: str, approved_cmd_list: list[str]) -> str:
    """
    Execute a user‑supplied command only if every token in the command is
    present in `approved_cmd_list`. The command is executed without a shell
    to avoid injection attacks.

    Parameters:
        cmd (str): The command string supplied by the user.
        approved_cmd_list (list[str]): A list of allowed subcommands.

    Returns:
        str: The standard output from the executed command, or an error
             message if execution fails.

    Raises:
        ValueError: If any token in the command is not in `approved_cmd_list`.
    """
    # Tokenise the user input safely
    try:
        tokens = shlex.split(cmd)
    except ValueError as e:
        raise ValueError(f"Failed to parse command: {e}") from None

    # Ensure each token is approved
    for t in tokens:
        if t not in approved_cmd_list:
            raise ValueError(f"Command token '{t}' is not allowed")

    # Execute the command without a shell
    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            check=False  # We handle errors ourselves
        )
    except Exception as exc:
        return f"Execution error: {exc}"

    # Return output or error message
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Command failed with exit code {result.returncode}: {result.stderr.strip()}"