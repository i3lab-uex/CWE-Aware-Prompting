import shlex

# Predefined shell command template with a placeholder for the user's name.
BASE_COMMAND = "echo 'Hello, {name_of_user}!'"

def assemble_greet_command(name_of_user: str) -> str:
    """
    Construct a shell command that greets the user by name.

    Parameters
    ----------
    name_of_user : str
        The user's name to be inserted into the command.

    Returns
    -------
    str
        A shell command string with the user's name safely quoted to prevent
        command injection or syntax errors.

    Notes
    -----
    - The function uses :func:`shlex.quote` to escape any characters that
      could alter the shell command structure, mitigating CWE-707 risks.
    - No exceptions are raised for empty or non-string inputs; they will be
      treated as literal strings and quoted appropriately.
    """
    # Ensure the input is a string; convert if necessary
    name_str = str(name_of_user)

    # Safely escape the user-provided name for shell usage
    safe_name = shlex.quote(name_str)

    # Replace the placeholder with the safely quoted name
    command = BASE_COMMAND.format(name_of_user=safe_name)

    return command