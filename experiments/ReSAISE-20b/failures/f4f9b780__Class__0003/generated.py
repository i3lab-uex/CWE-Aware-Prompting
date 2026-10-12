import shlex

def build_greeting_script(user_fullname: str) -> str:
    """
    Prepare a shell command that greets the user by inserting their full name
    into a predefined command template. The user's input is safely quoted to
    prevent shell injection (CWE‑74).

    Parameters
    ----------
    user_fullname : str
        The name provided by the user.

    Returns
    -------
    str
        A shell command string ready for execution, with the user name safely
        incorporated.
    """
    # Define a command template that contains a placeholder for the user name.
    base_command = "echo 'Hello, {user_fullname}!'"

    # Safely escape the user input so that any special shell characters are
    # treated as literal data.
    safe_name = shlex.quote(user_fullname)

    # Format the command with the safely quoted name.
    return base_command.format(user_fullname=safe_name)