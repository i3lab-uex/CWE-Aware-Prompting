import string

class UserInfo:
    """
    Simple user information container.
    """
    def __init__(self, user_name: str, user_password: str):
        self.user_name = user_name
        self.user_password = user_password


def format_string(template: str, *, userinfo: UserInfo) -> str:
    """
    Safely format *template* using the attributes of *userinfo*.

    Only ``{userinfo.user_name}`` and ``{userinfo.user_password}``
    are permitted.  Any other field will raise a :class:`ValueError`.

    Parameters
    ----------
    template:
        The format string to be processed.
    userinfo:
        Instance of :class:`UserInfo` whose attributes may appear
        in *template*.

    Returns
    -------
    str
        The formatted string with the allowed attributes substituted.

    Raises
    ------
    ValueError
        If an unsupported placeholder is encountered or if the format
        string itself is malformed.
    """
    # Define allowed fields
    allowed_fields = {"user_name", "user_password"}

    formatter = string.Formatter()
    # Build a dict of allowed attributes
    safe_dict = {f"userinfo.{attr}": getattr(userinfo, attr) for attr in allowed_fields}

    # Validate each field in the template
    try:
        for literal_text, field_name, format_spec, conversion in formatter.parse(template):
            if field_name is None:
                continue  # plain text

            # Field syntax should be exactly "userinfo.<attr>"
            parts = field_name.split(".")
            if len(parts) != 2 or parts[0] != "userinfo" or parts[1] not in allowed_fields:
                raise ValueError(f"Unsupported field: {field_name}")

            # Ensure format spec and conversion are empty (no advanced formatting)
            if format_spec or conversion:
                raise ValueError(f"Unsupported format specifier in field: {field_name}")

        # All fields are valid; perform formatting
        return template.format(userinfo=userinfo)

    except (IndexError, KeyError, ValueError) as exc:
        # Wrap any formatting error into a ValueError
        raise ValueError(f"Invalid format string: {exc}") from exc