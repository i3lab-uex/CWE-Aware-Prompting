import shlex

def build_greeting_script(user_fullname: str) -> str:
    """
    Prepare a shell command that greets the user by inserting their name into
    a predefined command template. The function safely escapes the supplied
    user input to prevent shell injection attacks.

    Parameters:
        user_fullname (str): The full name of the user to be inserted into
                             the command template.

    Returns:
        str: The final shell command with the user name safely quoted.
    """
    # Base command template. Replace '{user_fullname}' with the escaped user name.
    base_command = "echo 'Hello, {user_fullname}!'"

    # Sanitize the user input by quoting it for safe use in a shell context.
    escaped_name = shlex.quote(user_fullname)

    # Construct the final command by formatting with the escaped name.
    final_command = base_command.format(user_fullname=escaped_name)

    return final_command