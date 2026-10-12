import shlex

def build_greeting_script(user_fullname: str) -> str:
    """
    Prepare a shell command that greets the user.

    Parameters
    ----------
    user_fullname : str
        The name of the user to be inserted into the command.

    Returns
    -------
    str
        A shell command string that safely includes the user's name.
    """
    # Template with a placeholder for the user full name
    base_command = "echo 'Hello, {user_fullname}!'"

    # Sanitize the user input to prevent command injection
    safe_name = shlex.quote(user_fullname)

    # Replace the placeholder with the sanitized name
    final_command = base_command.format(user_fullname=safe_name)

    return final_command