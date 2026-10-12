import shlex

def create_greeting_command(username: str) -> str:
    """
    Prepare a shell command that greets the user.

    The function uses `shlex.quote` to safely escape any special
    characters in the username, preventing command injection.

    Parameters:
        username (str): The user supplied name to be inserted into the
                        command template.

    Returns:
        str: A shell command string that greets the user.
    """
    # Base command template containing a placeholder for the username
    base_command = "echo 'Hello, {username}! Welcome to our system.'"

    # Safely escape the username so that it cannot break out of the
    # single quotes in the template.
    safe_username = shlex.quote(username)

    # Substitute the escaped username into the command
    final_command = base_command.format(username=safe_username)

    return final_command