import shlex

# Predefined shell command template with a placeholder for the user's name.
BASE_COMMAND = "echo 'Hello, {name_of_user}! Welcome to the system.'"

def assemble_greet_command(name_of_user: str) -> str:
    """
    Construct a shell command that greets the user by inserting their name
    safely into the predefined template.

    Parameters:
        name_of_user (str): The user's name to be inserted into the command.

    Returns:
        str: A shell command string with the user's name safely quoted.
    """
    # Quote the user-provided name to prevent shell injection attacks.
    safe_name = shlex.quote(name_of_user)

    # Substitute the placeholder with the quoted name.
    command = BASE_COMMAND.format(name_of_user=safe_name)

    return command