import shlex

# Assume this function is provided elsewhere in the codebase.
def execute_command(command: str) -> None:
    """
    Executes a shell command. Implementation is omitted.
    """
    pass


def generate_greeting_command(user_name: str) -> str:
    """
    Generates a shell command that greets the user by name and executes it.

    Parameters
    ----------
    user_name : str
        The user-provided name to be embedded into the command.

    Returns
    -------
    str
        The generated shell command incorporating the user-provided name.
    """
    # Base command template with a placeholder for the username
    base_command = "echo \"Hello, {user_name}!\""

    # Sanitize the user input to prevent shell injection
    safe_user = shlex.quote(user_name)

    # Construct the final command by injecting the sanitized username
    command = base_command.format(user_name=safe_user)

    # Execute the constructed command (implementation omitted)
    execute_command(command)

    return command