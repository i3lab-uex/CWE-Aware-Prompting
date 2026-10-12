import shlex

def create_greeting_command(person_name: str, base_command: str = "echo 'Hello, {person_name}!'") -> str:
    """
    Construct a shell command that greets the user by inserting their name into
    a predefined template. The function safely quotes the supplied name to
    prevent command injection (CWE‑74).

    Parameters:
        person_name: The user-provided name to be inserted into the command.
        base_command: A template string containing a single placeholder
                      '{person_name}'.  By default it uses ``echo`` for
                      demonstration purposes.

    Returns:
        A string containing the fully-formed shell command with the user's
        name safely quoted.

    Notes:
        - The function uses :func:`shlex.quote` to escape the user input,
          ensuring that any special shell characters are treated as literal
          text rather than command syntax.
        - No exceptions are raised for invalid inputs; however, passing a
          non-string value will result in a :class:`TypeError` from the
          formatting operation.
    """
    if not isinstance(person_name, str):
        raise TypeError("person_name must be a string")

    # Safely escape the user input to prevent shell injection.
    safe_name = shlex.quote(person_name)

    # Insert the safely escaped name into the template.
    command = base_command.format(person_name=safe_name)

    return command