import shlex

# Base command template containing a placeholder for the username.
BASE_COMMAND = "echo 'Welcome, {username}!'"


def create_greeting_command(username: str) -> str:
    """
    Prepare a shell command that greets the user.

    The function safely inserts the provided username into the
    predefined command template.  It uses shlex.quote to escape any
    characters that could be interpreted by the shell, mitigating
    command‑injection risks.

    Parameters:
        username (str): The user name to include in the greeting.

    Returns:
        str: A fully‑formed shell command ready for execution.
    """
    # Quote the username to neutralize any special characters
    safe_username = shlex.quote(username)

    # Substitute the placeholder with the safely quoted username
    return BASE_COMMAND.format(username=safe_username)