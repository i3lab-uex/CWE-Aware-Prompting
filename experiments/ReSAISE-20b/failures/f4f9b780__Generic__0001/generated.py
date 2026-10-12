import shlex

# Base command template with a placeholder for the user full name.
BASE_COMMAND = "echo 'Hello, {user_fullname}!'"

def build_greeting_script(user_fullname: str) -> str:
    """
    Construct a shell command that greets the user by name.

    The supplied user_fullname is safely quoted to avoid shell injection
    vulnerabilities before it is inserted into the command template.

    Parameters
    ----------
    user_fullname : str
        The full name of the user to greet.

    Returns
    -------
    str
        A fully-formed shell command that can be executed safely.
    """
    # Quote the user input to make it safe for shell usage
    quoted_name = shlex.quote(user_fullname)

    # Substitute the placeholder with the safely quoted name
    command = BASE_COMMAND.format(user_fullname=quoted_name)

    return command