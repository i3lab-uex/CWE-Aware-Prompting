import shlex

# Command template with a placeholder for the user name.
BASE_COMMAND = "echo 'Hello, {user_fullname}!'"

def build_greeting_script(user_fullname: str) -> str:
    """
    Prepare a shell command that greets the user.
    
    The function safely incorporates the provided user name into the
    command by quoting it with shlex.quote, preventing shell injection.
    
    Parameters:
        user_fullname (str): The user's full name to include in the greeting.
    
    Returns:
        str: A shell command string ready for execution.
    """
    # Quote the user input to escape any special characters.
    safe_name = shlex.quote(user_fullname)
    
    # Insert the quoted name into the command template.
    return BASE_COMMAND.format(user_fullname=safe_name)