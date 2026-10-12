import shlex

# Base command template with a placeholder for the user name.
BASE_COMMAND = "echo 'Hello, {user_fullname}!'"

def build_greeting_script(user_fullname: str) -> str:
    """
    Build a safe shell command that greets the user.

    Parameters
    ----------
    user_fullname : str
        The full name of the user to be inserted into the command.

    Returns
    -------
    str
        A shell command string with the user name safely quoted.
    """
    # Use shlex.quote to escape any characters that could be interpreted by the shell
    safe_name = shlex.quote(user_fullname)

    # Replace the placeholder with the safely quoted name
    command = BASE_COMMAND.format(user_fullname=safe_name)

    return command