from dataclasses import dataclass

@dataclass
class UserInfo:
    """Simple user information holder."""
    user_name: str
    user_password: str

def format_string(string: str) -> str:
    """
    Format the given string using a UserInfo instance.

    The function will not expose sensitive information such as
    ``user_password``. If the format string attempts to access
    ``userinfo.user_password``, a ValueError is raised.

    Parameters
    ----------
    string : str
        The format string that may contain ``{userinfo.user_name}``.

    Returns
    -------
    str
        The formatted string.

    Raises
    ------
    ValueError
        If the format string contains a reference to ``userinfo.user_password``.
    """
    # Do not allow access to sensitive data
    if "user_password" in string:
        raise ValueError("Attempted to expose sensitive information.")

    # Create a user info instance with dummy data.
    # In real usage, replace this with actual authenticated user details.
    userinfo = UserInfo(user_name="anonymous", user_password="REDACTED")

    try:
        return string.format(userinfo=userinfo)
    except Exception as exc:
        raise ValueError(f"Formatting error: {exc}") from exc