# Authorize and validate a user-provided command against a trusted whitelist.

ALLOWED_COMMANDS = {
    "list_files",
    "show_date",
    "echo_hello",
    # Add other safe commands here
}

def authorize_and_run_cmd(command: str):
    """
    Validate a command against the ALLOWED_COMMANDS whitelist.

    Args:
        command (str): The user-provided command string.

    Returns:
        str | None: The original command if it is allowed, otherwise None.
    """
    # Strip whitespace to avoid accidental mismatches
    cleaned = command.strip()

    if cleaned in ALLOWED_COMMANDS:
        return cleaned

    # Optionally log or audit the denied attempt here
    return None