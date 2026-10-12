import shlex

# Base command template (for example: echo "Hello, {user_name}!")
base_command = 'echo "Hello, {user_name}!"'

def generate_greeting_command(user_name: str) -> str:
    """
    Generate a shell command that greets the user by name.

    Parameters
    ----------
    user_name : str
        The user-provided name to be embedded into the command.

    Returns
    -------
    str
        The generated shell command with the user name safely escaped.
    """
    # Use shlex.quote to escape any special characters that could lead
    # to command injection. This mitigates CWE-74.
    safe_name = shlex.quote(user_name)

    # Build the command by inserting the escaped name into the template.
    command = base_command.format(user_name=safe_name)

    return command