import re

# A predefined set of safe commands that the user is allowed to run.
ALLOWED_COMMANDS = {
    "list_files",
    "show_date",
    "display_uptime",
    # Add other safe command identifiers here.
}

def check_and_run_command(command_input: str) -> str | None:
    """
    Validate the user-provided command against a whitelist of allowed commands.

    Parameters
    ----------
    command_input : str
        The raw input string from the user representing a command.

    Returns
    -------
    str | None
        The exact command string if it is in ALLOWED_COMMANDS,
        otherwise None.

    Notes
    -----
    - The function normalises the input by stripping leading/trailing
      whitespace and converting to lower case, ensuring consistent matching.
    - No further sanitisation is required because only the command name itself
      is considered; no arguments or shell expansions are accepted.
    """
    # Normalise input: strip whitespace and collapse internal spaces
    cleaned = re.sub(r"\s+", " ", command_input.strip()).lower()

    # Check against the whitelist
    if cleaned in ALLOWED_COMMANDS:
        return cleaned

    return None