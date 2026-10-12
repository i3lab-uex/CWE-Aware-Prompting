import shlex

# Example command template that will greet the user.
# The placeholder `{username}` is replaced with a safely quoted value.
BASE_COMMAND = "echo 'Hello, {username}!'"


def create_greeting_command(username: str) -> str:
    """
    Return a shell command that greets the user, safely quoting the supplied
    username to avoid command injection (CWE‑74).

    Parameters
    ----------
    username : str
        The user supplied name to include in the command.

    Returns
    -------
    str
        A shell command that echoes a greeting containing the quoted username.
    """
    # Quote the user input so that any special characters are treated literally
    safe_username = shlex.quote(username)
    # Substitute the placeholder with the quoted username.
    return BASE_COMMAND.format(username=safe_username)