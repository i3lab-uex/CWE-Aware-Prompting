import shlex

# Predefined command template with a placeholder for the person's name.
BASE_COMMAND = "echo 'Hello, {person_name}! Welcome to the system.'"

def create_greeting_command(person_name: str) -> str:
    """
    Construct a shell command that greets the user by name.

    The function safely escapes the provided name to prevent shell injection
    attacks. It uses `shlex.quote` which returns a shell-escaped version of the
    string suitable for inclusion in a command line.

    Parameters:
        person_name (str): The name supplied by the user.

    Returns:
        str: A fully-formed shell command with the escaped name inserted.
    """
    # Ensure that person_name is a string; if not, convert it to str
    safe_name = shlex.quote(str(person_name))
    
    # Replace the placeholder with the escaped name
    command = BASE_COMMAND.format(person_name=safe_name)
    
    return command