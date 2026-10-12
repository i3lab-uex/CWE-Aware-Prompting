import shlex

def prepare_greet_command(user: str, base_command: str = "echo 'Hello, {user}!'" ) -> str:
    """
    Prepare a shell command that greets the user by safely inserting their name
    into the provided base_command template.

    Parameters:
        user (str): The user's name to insert into the command.
        base_command (str): A shell command template containing a single
            placeholder '{user}'. Defaults to "echo 'Hello, {user}!'" if not
            supplied.

    Returns:
        str: The fully formed shell command with the user's name safely escaped.

    Notes:
        - The function uses shlex.quote to neutralize any shell metacharacters
          in the user input, mitigating command injection risk.
        - If the placeholder '{user}' is missing from base_command, a
          ValueError is raised to prevent silent mis‑generation.
    """
    if "{user}" not in base_command:
        raise ValueError("base_command must contain a '{user}' placeholder")

    # Safely escape the user input
    safe_user = shlex.quote(user)

    # Substitute the placeholder with the escaped value
    command = base_command.replace("{user}", safe_user)

    return command