import string
from dataclasses import dataclass

@dataclass
class UserInfo:
    """Simple container for user credentials."""
    user_name: str
    user_password: str


def format_string(s: str) -> str:
    """
    Safely format *s* using a UserInfo instance.

    The input string may contain placeholders that reference the
    ``userinfo`` object (e.g. ``{userinfo.user_name}``).  No other
    placeholders are allowed.  The function raises a :class:`ValueError`
    if the string contains unsupported fields or if formatting fails.

    Parameters
    ----------
    s : str
        The string to format.

    Returns
    -------
    str
        The formatted string.

    Raises
    ------
    ValueError
        If the format string contains unsupported fields or if an error
        occurs during formatting.
    """
    # Instantiate a UserInfo object with placeholder values.
    # In real usage this would be populated from the server's user store.
    userinfo = UserInfo(user_name="placeholder", user_password="placeholder")

    # Validate that the format string only uses the 'userinfo' object.
    formatter = string.Formatter()
    for literal_text, field_name, format_spec, conversion in formatter.parse(s):
        # Skip literals that don't contain a field.
        if field_name is None:
            continue

        # A field can be nested like "userinfo.user_name" or just "userinfo".
        parts = field_name.split('.')
        if len(parts) == 1:
            # e.g. "{userinfo}"
            if parts[0] != "userinfo":
                raise ValueError(f"Unsupported field: {field_name}")
        else:
            # e.g. "{userinfo.user_name}"
            if parts[0] != "userinfo":
                raise ValueError(f"Unsupported field: {field_name}")

    try:
        result = s.format(userinfo=userinfo)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Formatting error: {exc}") from exc

    return result