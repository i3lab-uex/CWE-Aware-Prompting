import shlex

# Predefined template for the shell command.
# The placeholder `{name_of_user}` will be replaced with a safely escaped value.
BASE_COMMAND = "echo 'Hello, {name_of_user}!'"

def assemble_greet_command(name_of_user: str) -> str:
    """
    Construct a shell command that greets the user by name.

    The function safely escapes the supplied `name_of_user` using
    :func:`shlex.quote`, preventing shell injection attacks (CWE-74).

    Args:
        name_of_user: The user's name to be inserted into the command.

    Returns:
        A string containing the fully formed shell command with the
        name safely quoted.
    """
    # Ensure the input is a string; coerce other types to str.
    if not isinstance(name_of_user, str):
        name_of_user = str(name_of_user)

    # Safely escape the user-provided string for shell usage.
    safe_name = shlex.quote(name_of_user)

    # Replace the placeholder with the quoted name.
    command = BASE_COMMAND.format(name_of_user=safe_name)

    return command