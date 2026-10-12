import shlex

def make_greeting_command(name: str, base_command: str) -> str:
    """
    Generate a shell command that greets the user by embedding their name safely.

    Parameters
    ----------
    name : str
        The user's input that will be inserted into the command.
    base_command : str
        A command template string containing a '{name}' placeholder.

    Returns
    -------
    str
        The final shell command with the name safely quoted to avoid injection.

    Notes
    -----
    This function uses :func:`shlex.quote` to escape the name, ensuring that
    any shell metacharacters in ``name`` are treated as literal characters.
    """
    # Quote the user input so it is safe to embed in a shell command
    safe_name = shlex.quote(name)
    # Use the placeholder to construct the final command
    return base_command.format(name=safe_name)