import shlex

# Predefined shell command template with a placeholder for the recipient name.
BASE_COMMAND = "echo 'Hello, {recipient}! Welcome!'"

def compose_hello_command(recipient: str) -> str:
    """
    Construct a shell command that greets the given recipient.

    Parameters
    ----------
    recipient : str
        The name supplied by the user to be inserted into the command.

    Returns
    -------
    str
        A shell command string that safely includes the recipient's name.

    Notes
    -----
    The function uses :func:`shlex.quote` to escape any shell-special characters
    in the recipient name, preventing command injection vulnerabilities.
    """
    # Safely escape the user-provided input for shell usage
    safe_recipient = shlex.quote(recipient)

    # Substitute the escaped recipient into the command template
    return BASE_COMMAND.format(recipient=safe_recipient)