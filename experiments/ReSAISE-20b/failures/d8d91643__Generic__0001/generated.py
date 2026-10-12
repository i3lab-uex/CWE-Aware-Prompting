import shlex

def build_greeting_command(nickname: str, base_command: str = "echo 'Hello, {nickname}!'") -> str:
    """
    Build a shell command that greets the user, safely embedding the provided nickname.

    Parameters
    ----------
    nickname : str
        The user supplied name to be inserted into the command.
    base_command : str, optional
        A template string containing a '{nickname}' placeholder. Default is
        "echo 'Hello, {nickname}!'".

    Returns
    -------
    str
        The final shell command with the nickname safely quoted.
    """
    # Use shlex.quote to escape any characters that could be interpreted by the shell.
    safe_nickname = shlex.quote(nickname)
    return base_command.format(nickname=safe_nickname)