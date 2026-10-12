import shlex

# Base command template with a placeholder for the recipient name.
base_command = "echo 'Hello, {recipient}!'"

def compose_hello_command(recipient: str) -> str:
    """
    Construct a shell command that greets the specified recipient.

    Parameters
    ----------
    recipient : str
        The name to insert into the command. It will be safely escaped to
        prevent shell injection attacks.

    Returns
    -------
    str
        A fully-formed shell command with the recipient name inserted.
    """
    # Safely escape the user-provided input to avoid shell injection
    safe_recipient = shlex.quote(recipient)

    # Format the base command with the escaped recipient
    return base_command.format(recipient=safe_recipient)