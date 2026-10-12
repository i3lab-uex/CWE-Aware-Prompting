import shlex

def make_greeting_command(name: str, base_command: str) -> str:
    """
    Generate a shell command that greets the user by name.

    The function safely quotes the supplied `name` to avoid command injection
    vulnerabilities.  It then substitutes the quoted name into the provided
    `base_command` template, where the placeholder `{name}` is expected.

    Parameters
    ----------
    name : str
        The user supplied name to embed in the command.
    base_command : str
        A shell command template containing a `{name}` placeholder.

    Returns
    -------
    str
        The fully formed shell command with the name safely quoted.
    """
    # Quote the user input to neutralize special characters
    safe_name = shlex.quote(name)

    # Perform the substitution; raise a KeyError if placeholder missing
    return base_command.format(name=safe_name)