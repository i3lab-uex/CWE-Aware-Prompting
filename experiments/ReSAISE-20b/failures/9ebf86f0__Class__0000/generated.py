import shlex

# Base command template used for greeting.
# Example: "echo 'Hello, {user_name}!'" or any other shell command that accepts a name.
base_command = "echo 'Hello, {user_name}!'"


def generate_greeting_command(user_name: str) -> str:
    """
    Generate a shell command that greets the user by name.

    Parameters
    ----------
    user_name : str
        The user-provided name to embed into the command.

    Returns
    -------
    str
        A shell command string with the user name safely quoted.
    """
    # Safely quote the user supplied value to prevent command injection.
    safe_name = shlex.quote(user_name)
    # Replace the placeholder with the quoted name
    command = base_command.format(user_name=safe_name)
    return command