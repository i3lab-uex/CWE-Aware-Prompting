import shlex

# Base command template with a placeholder for the person's name.
BASE_COMMAND = "echo 'Hello, {person_name}!'"


def create_greeting_command(person_name: str) -> str:
    """
    Construct a shell command that greets the user by name.

    The function safely quotes the provided name to avoid shell injection
    vulnerabilities. It replaces the placeholder in BASE_COMMAND with the
    quoted name and returns the final command string.

    Parameters
    ----------
    person_name : str
        The name to greet. This value is sanitized before being inserted into the command.

    Returns
    -------
    str
        A shell command that prints a greeting message containing the given name.
    """
    # Sanitize the input by quoting it for safe shell usage.
    quoted_name = shlex.quote(person_name)

    # Build the command by inserting the quoted name into the template.
    command = BASE_COMMAND.format(person_name=quoted_name)

    return command