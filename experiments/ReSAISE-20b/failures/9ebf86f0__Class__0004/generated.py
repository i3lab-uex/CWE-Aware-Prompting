import shlex

# Assume this function exists elsewhere in the codebase.
def execute_command(cmd: str) -> None:
    """Executes a shell command. Implementation is omitted."""
    pass


def generate_greeting_command(user_name: str) -> str:
    """
    Generates a shell command that greets the user by name.

    Parameters
    ----------
    user_name : str
        The user-provided name to be embedded into the command.

    Returns
    -------
    str
        The fully-formed shell command incorporating the sanitized user name.

    Notes
    -----
    The function uses :func:`shlex.quote` to escape any special characters in
    ``user_name``.  This mitigates CWE-74 by preventing command injection.
    """
    # Base command template with a placeholder for the user name
    base_command = "echo 'Hello, {user_name}! Welcome to our system.'"

    # Sanitize the user-provided name
    safe_user_name = shlex.quote(user_name)

    # Construct the final command string
    command = base_command.format(user_name=safe_user_name)

    # Optionally execute the command (commented out because implementation is omitted)
    # execute_command(command)

    return command