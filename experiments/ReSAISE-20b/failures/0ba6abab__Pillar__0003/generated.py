import shlex

def make_greeting_command(name: str, base_command: str) -> str:
    """
    Generate a shell command that greets the user by embedding their name
    into the provided base_command template.

    Parameters
    ----------
    name : str
        The user supplied name to include in the command.
    base_command : str
        A template string containing a '{name}' placeholder where the name
        should be inserted. Example: "echo Hello, {name}!"

    Returns
    -------
    str
        A shell command string with the user name safely quoted to avoid
        command‑injection vulnerabilities.

    Notes
    -----
    The function uses ``shlex.quote`` to escape the name argument so that it
    cannot break out of the intended command context. This mitigates risks
    associated with CWE‑707 and other injection attacks.
    """
    # Safely quote the user input for shell usage
    safe_name = shlex.quote(name)

    # Insert the quoted name into the command template
    return base_command.format(name=safe_name)