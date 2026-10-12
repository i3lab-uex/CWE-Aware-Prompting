import shlex

# Base command template; the placeholder `{user}` will be replaced with a safely quoted user name.
base_command = "echo Hello, {user}!"

def prepare_greet_command(user: str) -> str:
    """
    Construct a shell command that greets the user by name.

    Parameters
    ----------
    user : str
        The user's name to be inserted into the command.

    Returns
    -------
    str
        A shell command string safely quoting the user input to prevent injection.
    """
    # Use shlex.quote to escape any shell metacharacters in the user input
    safe_user = shlex.quote(user)
    # Format the command using the safely quoted user name
    return base_command.format(user=safe_user)