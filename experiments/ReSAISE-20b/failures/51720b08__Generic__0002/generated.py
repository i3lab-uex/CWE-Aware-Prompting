import shlex

def compose_hello_command(recipient: str) -> str:
    """
    Construct a shell command that greets the specified recipient.

    Parameters
    ----------
    recipient : str
        The name to be inserted into the command.  It is safely quoted to
        prevent shell injection.

    Returns
    -------
    str
        The complete shell command with the recipient name embedded.
    """
    # Predefined base command template
    base_command = "echo 'Hello, {recipient}! Welcome!'"

    # Safely escape the recipient string
    safe_recipient = shlex.quote(recipient)

    # Format the command with the quoted recipient
    return base_command.format(recipient=safe_recipient)