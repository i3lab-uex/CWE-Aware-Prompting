import shlex

def create_greeting_command(username: str) -> str:
    """
    Prepare a shell command that greets the user by inserting their name
    into a predefined command template.

    Parameters:
        username (str): The user-provided name to be included in the command.

    Returns:
        str: A shell command string that safely incorporates the username.
             The username is escaped using shlex.quote to mitigate
             command‑injection risks.

    Example:
        >>> create_greeting_command("Alice")
        'echo "Hello, Alice!"'
    """
    # Base command template with a placeholder for the username
    base_command = 'echo "Hello, {username}!"'

    # Sanitize the username to prevent shell injection
    safe_username = shlex.quote(username)

    # Insert the sanitized username into the command template
    final_command = base_command.format(username=safe_username)

    return final_command