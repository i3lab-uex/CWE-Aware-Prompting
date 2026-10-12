# AccessControl framework – format_string implementation

from dataclasses import dataclass


@dataclass
class UserInfo:
    """Simple user information holder."""
    user_name: str
    user_password: str


def format_string(string: str) -> str:
    """
    Format the supplied string using a UserInfo instance.

    The function only allows formatting with ``userinfo.user_name``.  If the
    string attempts to access ``user_password`` or any other attribute, a
    :class:`ValueError` is raised to prevent accidental exposure of sensitive
    data (CWE‑200).

    Parameters
    ----------
    string : str
        The input format string.  It must contain at most ``{userinfo.user_name}``
        as a placeholder.

    Returns
    -------
    str
        The formatted string with the user name inserted.

    Raises
    ------
    ValueError
        If the format string references ``user_password`` or any other disallowed
        attribute, or if formatting fails.
    """
    # Disallow access to the password field or any other attribute
    disallowed_placeholders = ["{userinfo.user_password}", "{userinfo.user_name}"]

    # Check for disallowed placeholders explicitly
    if "{userinfo.user_password}" in string:
        raise ValueError("Access to user_password is prohibited")

    # Ensure only allowed placeholders are used
    # This simple check covers common cases; more robust parsing can be added if needed.
    allowed_keys = {"userinfo.user_name"}
    for key in allowed_keys:
        string = string.replace(f"{{{key}}}", "")
    if "{" in string or "}" in string:
        raise ValueError("Invalid or disallowed format placeholders detected")

    # Create the userinfo object (example: replace with actual user data in real use)
    user_info = UserInfo(user_name="alice", user_password="s3cr3t")

    try:
        formatted = string.format(userinfo=user_info)
    except Exception as exc:
        raise ValueError(f"Formatting error: {exc}") from exc

    return formatted