import shlex

def prepare_greet_command(user: str) -> str:
    """
    Prepare a shell command that greets the user by inserting their name into
    a predefined command template. The user's input is safely escaped to avoid
    shell injection vulnerabilities.

    Parameters
    ----------
    user : str
        The name of the user to greet.

    Returns
    -------
    str
        A fully formed shell command ready for execution.
    """
    # Define the base command template. The placeholder `{user}` will be replaced
    # with a safely escaped user name.
    base_command = "echo 'Hello, {user}!'"

    # Use shlex.quote to escape any shell metacharacters in the user input.
    safe_user = shlex.quote(user)

    # Substitute the escaped name into the command template.
    final_command = base_command.format(user=safe_user)

    return final_command