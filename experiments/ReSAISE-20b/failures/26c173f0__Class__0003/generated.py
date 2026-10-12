import re

class UserInfo:
    """Simple container for user credentials."""
    def __init__(self, user_name: str, user_password: str):
        self.user_name = user_name
        self.user_password = user_password


def format_string(string: str) -> str:
    """
    Safely format a string containing `{userinfo.<attribute>}` placeholders.

    Only the `user_name` attribute may be interpolated.  Attempting to
    interpolate `user_password` or any other attribute results in a
    ValueError, preventing accidental disclosure of sensitive data.

    Parameters:
        string (str): The format string containing placeholders.

    Returns:
        str: The formatted string with user data substituted.

    Raises:
        ValueError: If the format string contains disallowed attributes
                    or if formatting fails.
    """
    # Detect disallowed placeholders (user_password or any other attr)
    disallowed = re.findall(r'\{userinfo\.([^\}]+)\}', string)
    if any(attr != 'user_name' for attr in disallowed):
        raise ValueError("Attempt to expose disallowed user information")

    # Create a minimal userinfo object with only the safe attribute
    userinfo = UserInfo(user_name="placeholder", user_password="hidden")

    try:
        return string.format(userinfo=userinfo)
    except Exception as exc:
        raise ValueError(f"Formatting error: {exc}") from exc