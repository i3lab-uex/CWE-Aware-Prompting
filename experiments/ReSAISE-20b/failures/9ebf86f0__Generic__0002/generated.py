import shlex

# A simple placeholder for the command execution function.
# In real usage this would be imported from your utilities module.
def execute_command(cmd: str) -> None:
    """Execute the given shell command."""
    # Implementation omitted; assume it runs `cmd` safely.
    pass


# Base command template with a placeholder for the user name.
base_command = "echo \"Hello, {user_name}!\""


def generate_greeting_command(user_name: str) -> str:
    """
    Generate a shell command that greets the user by name.

    The function safely escapes the provided `user_name` to prevent
    shell injection attacks. It then substitutes the escaped name into
    the `base_command` template.

    Args:
        user_name: The name provided by the user to be embedded in
            the greeting.

    Returns:
        A string containing the fully formed shell command ready to be
        executed by `execute_command`.

    Raises:
        None.  (The function performs basic sanitization but does not
                raise exceptions on its own.)
    """
    # Use shlex.quote to escape the user input for shell usage.
    safe_name = shlex.quote(user_name)

    # Format the base command with the escaped user name.
    command = base_command.format(user_name=safe_name)

    return command


# Example usage:
if __name__ == "__main__":
    name = "Alice; rm -rf /"
    cmd = generate_greeting_command(name)
    print("Generated command:", cmd)  # Shows safe escaping
    execute_command(cmd)