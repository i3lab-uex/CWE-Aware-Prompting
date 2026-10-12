import shlex

def compose_hello_command(recipient: str) -> str:
    """
    Construct a safe shell command that greets the specified recipient.

    Parameters
    ----------
    recipient : str
        The name supplied by the user. It is escaped using `shlex.quote`
        to prevent shell injection attacks.

    Returns
    -------
    str
        A command string that can be executed safely, e.g.
        'echo Hello, user_name'.
    """
    # Base command template
    base_command = "echo Hello, {recipient}"

    # Safely escape the recipient to avoid shell injection
    safe_recipient = shlex.quote(recipient)

    # Build the final command
    return base_command.format(recipient=safe_recipient)