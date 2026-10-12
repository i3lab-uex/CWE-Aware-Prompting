import shlex

def assemble_greet_command(name_of_user: str, base_command: str) -> str:
    """
    Construct a shell command that greets the user by inserting their name into
    a predefined template. The user's input is safely escaped to avoid shell
    injection (CWE‑74).

    Parameters
    ----------
    name_of_user : str
        The user supplied name to be inserted into the command.
    base_command : str
        A template string containing a placeholder '{name_of_user}' where the
        name should appear.

    Returns
    -------
    str
        A fully-formed shell command with the name safely quoted.
    """
    # Escape any special shell characters in the user input
    safe_name = shlex.quote(name_of_user)

    # Insert the escaped name into the template
    return base_command.format(name_of_user=safe_name)