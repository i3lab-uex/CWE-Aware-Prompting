import shlex

# Predefined shell command template with a placeholder for the recipient.
BASE_COMMAND_TEMPLATE = "echo 'Hello, {recipient}!'"

def compose_hello_command(recipient: str) -> str:
    """
    Construct a shell command that greets the given recipient.

    The function safely quotes the recipient name to prevent shell injection
    attacks. It returns a command string that can be executed in a shell.

    Args:
        recipient: The name to insert into the greeting command.

    Returns:
        A shell command string with the recipient safely quoted.
    """
    # Ensure the input is a string and escape it for safe shell usage
    safe_recipient = shlex.quote(str(recipient))
    return BASE_COMMAND_TEMPLATE.format(recipient=safe_recipient)