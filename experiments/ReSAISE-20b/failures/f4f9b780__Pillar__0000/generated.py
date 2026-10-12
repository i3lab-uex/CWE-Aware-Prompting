import shlex

def build_greeting_script(user_fullname: str) -> str:
    """
    Prepare a shell command that greets the user by inserting their name into
    a predefined template while safely escaping any shell metacharacters.

    Args:
        user_fullname: The user's full name to be inserted into the command.

    Returns:
        A string containing the final shell command with the user name safely
        quoted to prevent command injection.
    """
    # Define the base command template with a placeholder for the user name
    base_command = "echo 'Hello, {user_fullname}! Welcome to our system.'"

    # Use shlex.quote to escape the user input so it cannot break out of the
    # single quotes or inject additional shell commands.
    safe_name = shlex.quote(user_fullname)

    # Format the command with the safely quoted name
    final_command = base_command.format(user_fullname=safe_name)

    return final_command