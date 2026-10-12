import shlex

# Predefined shell command template with a placeholder for the person's name.
BASE_COMMAND = "echo 'Hello, {person_name}! Welcome to the system.'"

def create_greeting_command(person_name: str) -> str:
    """
    Construct a shell command that greets the user with their name.

    Parameters
    ----------
    person_name : str
        The user's name to be inserted into the command.

    Returns
    -------
    str
        A shell command string with the user's name safely quoted.
    """
    # Quote the user-provided name to prevent shell injection attacks.
    safe_name = shlex.quote(person_name)
    # Insert the quoted name into the command template.
    return BASE_COMMAND.format(person_name=safe_name)