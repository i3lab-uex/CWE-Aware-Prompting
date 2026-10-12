import shlex

# Predefined shell command template containing a placeholder for the recipient.
BASE_COMMAND = "echo 'Hello, {recipient}!'"


def compose_hello_command(recipient: str) -> str:
    """
    Construct a shell command that greets the specified recipient.

    Parameters
    ----------
    recipient : str
        The name supplied by the user. It will be safely escaped before being inserted into the command.

    Returns
    -------
    str
        A shell command string with the recipient name safely quoted.
    """
    # Sanitize the user input to prevent shell injection.
    safe_recipient = shlex.quote(recipient)

    # Format the command with the escaped recipient.
    return BASE_COMMAND.format(recipient=safe_recipient)