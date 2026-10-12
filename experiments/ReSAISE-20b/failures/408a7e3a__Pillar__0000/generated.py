import shlex

def create_greeting_command(username: str) -> str:
    """
    Prepare a shell command that greets the user by inserting their name into
    a predefined command template. The username is safely quoted to prevent
    command injection.

    Parameters:
        username (str): The user-provided name.

    Returns:
        str: A shell command string with the username safely incorporated.
    """
    # Template command containing a placeholder for the username
    base_command = "echo 'Hello, {username}! Welcome to our system.'"

    # Safely escape the username for shell usage
    safe_username = shlex.quote(username)

    # Substitute the placeholder with the quoted username
    final_command = base_command.format(username=safe_username)

    return final_command