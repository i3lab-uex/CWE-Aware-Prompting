import re
from dataclasses import dataclass

@dataclass
class UserInfo:
    """Simple container for user credentials."""
    user_name: str
    user_password: str


def format_string(string: str) -> str:
    """
    Safely format a string containing only `{userinfo.user_name}` or
    `{userinfo.user_password}` placeholders.

    Parameters
    ----------
    string : str
        The input template string.

    Returns
    -------
    str
        The formatted string with placeholders replaced by the values from a
        temporary UserInfo instance.

    Raises
    ------
    ValueError
        If the string contains disallowed placeholders or formatting fails.
    """
    # Regular expression to capture all placeholders of the form {something}
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")

    # Find all placeholders
    placeholders = placeholder_pattern.findall(string)

    # Only allow 'userinfo.user_name' and 'userinfo.user_password'
    allowed = {"userinfo.user_name", "userinfo.user_password"}
    for ph in placeholders:
        if ph not in allowed:
            raise ValueError(f"Disallowed placeholder: {{{ph}}}")

    # Create a temporary UserInfo instance with dummy data
    temp_user = UserInfo(user_name="dummy", user_password="dummy")

    # Build a mapping that mimics the expected format syntax
    # The format string expects an object named 'userinfo', so we provide it
    mapping = {"userinfo": temp_user}

    try:
        formatted = string.format(**mapping)
    except Exception as exc:
        raise ValueError(f"Formatting error: {exc}") from exc

    return formatted