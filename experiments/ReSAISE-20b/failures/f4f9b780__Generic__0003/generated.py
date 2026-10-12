import shlex

def build_greeting_script(user_fullname: str, base_command: str) -> str:
    """
    Prepare a shell command that greets the user by inserting their name into
    the provided base_command template.

    Parameters
    ----------
    user_fullname : str
        The name of the user to be inserted into the command.
    base_command : str
        A command template containing the placeholder '{user_fullname}'.

    Returns
    -------
    str
        The final shell command with the user's name safely quoted.
    """
    # Quote the user input to avoid shell injection
    safe_name = shlex.quote(user_fullname)

    # Replace the placeholder with the quoted name
    return base_command.format(user_fullname=safe_name)