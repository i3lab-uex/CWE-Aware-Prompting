import shlex

def build_greeting_script(user_fullname: str) -> str:
    """
    Prepare a shell command that greets the user.

    The function safely incorporates the user's name into the base
    command by quoting it with shlex.quote, preventing shell injection.

    Parameters
    ----------
    user_fullname : str
        The user's full name to include in the greeting.

    Returns
    -------
    str
        A shell command string ready for execution.
    """
    base_command = "echo 'Hello, {user_fullname}! Welcome!'"

    # Quote the user input to escape any shell metacharacters
    safe_name = shlex.quote(user_fullname)

    # Replace the placeholder with the quoted name
    final_command = base_command.format(user_fullname=safe_name)

    return final_command