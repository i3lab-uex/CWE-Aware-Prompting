import os
import shlex
import subprocess

def filter_and_run_command(cmd_input: str, permitted_subcommands: list) -> str:
    """
    Execute a shell command only if all subcommands are in the permitted list.

    Parameters
    ----------
    cmd_input : str
        The full command string to execute.
    permitted_subcommands : list[str]
        List of subcommand tokens considered safe.

    Returns
    -------
    str
        The stdout output from the executed command if successful, or an error
        message indicating that the command was not allowed.

    Raises
    ------
    ValueError
        If any subcommand in the command is not present in `permitted_subcommands`.
    """
    # Safely split the input into tokens
    try:
        tokens = shlex.split(cmd_input)
    except ValueError as e:
        raise ValueError(f"Invalid command syntax: {e}") from e

    if not tokens:
        raise ValueError("Empty command string provided")

    # The first token is the program; all subsequent tokens are subcommands
    subcommands = tokens[1:]

    # Validate each subcommand against the allowed list
    for cmd in subcommands:
        if cmd not in permitted_subcommands:
            raise ValueError(f"Command '{cmd}' is not allowed")

    # Execute the command and capture output
    try:
        result = subprocess.run(
            tokens,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
    except subprocess.CalledProcessError as e:
        # Return the output even if the command failed
        return f"Command execution failed:\n{e.stdout}"
    except Exception as e:
        # Unexpected errors
        return f"Unexpected error during command execution: {e}"

    return result.stdout

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     allowed = ["-l", "-a"]
#     print(filter_and_run_command("ls -l", allowed))