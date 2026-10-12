import string
from dataclasses import dataclass

@dataclass(frozen=True)
class UserInfo:
    """Simple container for user credentials."""
    user_name: str
    user_password: str


def format_string(template: str, *, userinfo: UserInfo) -> str:
    """
    Safely format a template string that may contain `{userinfo.<attr>}` placeholders.

    Parameters
    ----------
    template : str
        The string to format. It may contain placeholders such as
        `{userinfo.user_name}` or `{userinfo.user_password}`.
    userinfo : UserInfo
        The instance providing the values for placeholders.

    Returns
    -------
    str
        The formatted string with placeholders replaced by the values from
        `userinfo`.

    Raises
    ------
    ValueError
        If formatting fails for any reason (e.g., missing attribute, invalid
        format string).
    """
    # Build a mapping that only exposes the allowed attributes.
    mapping = {"userinfo": userinfo}

    try:
        # Use format_map to avoid the default string.format which would treat
        # braces as literal if missing attributes.
        return template.format_map(mapping)
    except (KeyError, IndexError, ValueError) as exc:
        # Wrap any formatting exception in a ValueError for the caller.
        raise ValueError(f"Formatting error: {exc}") from exc


# Example usage (for testing purposes only; remove in production)
if __name__ == "__main__":
    ui = UserInfo(user_name="alice", user_password="secret")
    try:
        print(format_string("Hello {userinfo.user_name}! Your password is {userinfo.user_password}.", userinfo=ui))
    except ValueError as e:
        print(f"Error: {e}")