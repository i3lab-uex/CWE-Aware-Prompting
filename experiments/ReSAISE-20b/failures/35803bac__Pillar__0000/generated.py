import shlex

# Base template for the shell command. The placeholder `{person_name}` will be replaced
# with a safely quoted user-provided name.
BASE_COMMAND = "echo 'Hello, {person_name}!'"

def create_greeting_command(person_name: str) -> str:
    """
    Construct a shell command that greets the user by name.

    The function uses `shlex.quote` to safely escape the supplied name,
    preventing shell injection vulnerabilities (CWE-107) and ensuring
    proper neutralization of the input data.

    Parameters:
        person_name (str): The name to insert into the greeting command.

    Returns:
        str: A shell command string with the user's name safely quoted.
    """
    # Quote the user input to make it safe for inclusion in a shell command
    safe_name = shlex.quote(person_name)

    # Format the base command with the quoted name
    return BASE_COMMAND.format(person_name=safe_name)