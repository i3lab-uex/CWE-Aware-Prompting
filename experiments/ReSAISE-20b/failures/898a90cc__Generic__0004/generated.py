import re
from typing import Optional, Set

# Define the set of safe commands.  These should be kept minimal and
# only contain exact, fully-qualified command names.
ALLOWED_COMMANDS: Set[str] = {
    "ls",
    "cat",
    "echo",
    "pwd",
    # Add more safe commands as needed
}

def verify_and_run_command(cmd_input: str) -> Optional[str]:
    """
    Verify that a user-supplied command is in the list of allowed commands.
    
    Parameters
    ----------
    cmd_input : str
        The raw command string supplied by the user.
    
    Returns
    -------
    Optional[str]
        The command string if it is allowed; otherwise, ``None``.
    
    Notes
    -----
    * The function performs a **case-sensitive** match against the command name.
      If you need case-insensitive matching, adjust the comparison accordingly.
    * Only the command name itself is checked; arguments are not validated.
      If argument validation is required, add a more sophisticated parser
      (e.g., using `shlex.split`).
    * The function does **not** execute the command; it merely verifies
      that the command is safe to run. Execution should be performed
      elsewhere with appropriate safeguards (e.g., using subprocess).
    """
    
    # Strip leading/trailing whitespace to avoid accidental mismatches.
    cmd_clean = cmd_input.strip()
    
    # Extract the command name (the first word).
    match = re.match(r"(?P<cmd>\S+)", cmd_clean)
    if not match:
        return None
    
    command_name = match.group("cmd")
    
    # Check if the extracted command is in the allowed list.
    if command_name not in ALLOWED_COMMANDS:
        return None
    
    # At this point, the command is considered safe.
    return cmd_clean