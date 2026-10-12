import shlex

# Predefined shell command template with a placeholder for the user name.
BASE_COMMAND_TEMPLATE = "echo 'Hello, {name_of_user}! Welcome to the system.'"

def assemble_greet_command(name_of_user: str) -> str:
    """
    Construct a shell command that greets the user by name, safely escaping
    the input to prevent command injection.

    Parameters:
        name_of_user (str): The user-provided name to include in the greeting.

    Returns:
        str: A shell command string with the user's name safely inserted.
    """
    # Use shlex.quote to escape any special characters in the user input,
    # ensuring that the resulting command cannot be manipulated by injection.
    safe_name = shlex.quote(name_of_user)

    # Replace the placeholder with the safely quoted name.
    command = BASE_COMMAND_TEMPLATE.format(name_of_user=safe_name)

    return command