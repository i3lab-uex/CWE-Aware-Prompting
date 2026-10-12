import shlex

def build_greeting_script(user_fullname: str) -> str:
    """
    Build a shell command that greets the user, safely incorporating the
    provided name into the command string.

    Parameters:
        user_fullname (str): The user's full name to be included in the command.

    Returns:
        str: A shell command string with the user name properly escaped.
    """
    # Define a base command template.  The placeholder will be replaced by the
    # escaped user name.
    base_command = "echo 'Hello, {user_fullname}!'"

    # Escape the user supplied name so that it cannot break out of the
    # single‑quoted string in the command.  `shlex.quote` adds quotes around
    # the argument and escapes any internal characters that could be
    # interpreted by the shell.
    safe_name = shlex.quote(user_fullname)

    # Replace the placeholder with the escaped name.
    return base_command.format(user_fullname=safe_name)