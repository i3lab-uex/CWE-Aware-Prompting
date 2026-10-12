import string
from dataclasses import dataclass

@dataclass
class UserInfo:
    """Simple container for user information."""
    user_name: str
    user_password: str


def format_string(string_to_format: str) -> str:
    """
    Format *string_to_format* using only the attributes of a UserInfo instance.

    Parameters
    ----------
    string_to_format : str
        The input string. It may contain placeholders such as
        ``{userinfo.user_name}`` or ``{userinfo.user_password}``.

    Returns
    -------
    str
        The formatted string.

    Raises
    ------
    ValueError
        If the string contains an unsupported placeholder or if formatting fails.
    """
    allowed_fields = {"userinfo.user_name", "userinfo.user_password"}

    # Verify that the string contains only allowed fields.
    formatter = string.Formatter()
    for literal_text, field_name, format_spec, conversion in formatter.parse(string_to_format):
        if field_name is None:
            continue  # literal text
        # Remove any conversion or format spec from the field name
        if field_name not in allowed_fields:
            raise ValueError(f"Unsupported placeholder: {{{field_name}}}")

    # Perform the formatting with a UserInfo instance.
    try:
        userinfo = UserInfo(user_name="dummy", user_password="dummy")
        result = string_to_format.format(userinfo=userinfo)
    except Exception as exc:
        raise ValueError(f"Formatting failed: {exc}") from exc

    return result