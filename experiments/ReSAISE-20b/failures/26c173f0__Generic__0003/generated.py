import re
from dataclasses import dataclass

@dataclass
class UserInfo:
    """Simple container for user credentials."""
    user_name: str
    user_password: str


def format_string(string: str) -> str:
    """
    Format *string* using a ``UserInfo`` instance.

    The input string may contain format fields that reference the
    ``user_name`` or ``user_password`` attributes of a :class:`UserInfo`
    instance, e.g. ``"{userinfo.user_name}"`` or
    ``"{userinfo.user_password}"``.

    Parameters
    ----------
    string : str
        The format template.

    Returns
    -------
    str
        The formatted string with the user information inserted.

    Raises
    ------
    ValueError
        If the format string contains an unsupported field, or if any other
        error occurs during formatting.
    """
    # Only allow the two specific fields to be used in the format string
    allowed_fields = {"user_name", "user_password"}
    # Regex to find all field names in the format string
    pattern = re.compile(r"{([^{}]+)}")
    for match in pattern.finditer(string):
        field = match.group(1).strip()
        # The format string may include a leading name (e.g. userinfo.)
        if field.startswith("userinfo."):
            field = field[len("userinfo.") :]
        # Reject any unsupported field
        if field not in allowed_fields:
            raise ValueError(f"Unsupported format field: {field!r}")

    # Construct a UserInfo instance with dummy data (the actual values
    # would normally come from the authenticated user context).
    # Here we just provide placeholders to satisfy formatting.
    dummy_user = UserInfo(user_name="dummy", user_password="dummy")

    try:
        return string.format(userinfo=dummy_user)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to format string: {exc}") from exc