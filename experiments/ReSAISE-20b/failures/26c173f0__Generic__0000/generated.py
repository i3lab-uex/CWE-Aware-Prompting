import re

# Minimal UserInfo class for demonstration.
class UserInfo:
    def __init__(self, user_name: str, user_password: str):
        self.user_name = user_name
        self.user_password = user_password

# Example global instance (in real use this would come from your server context)
CURRENT_USER = UserInfo(user_name="alice", user_password="s3cr3t")

# Allowed placeholders – only the two attributes of UserInfo
_ALLOWED_PLACEHOLDERS = {"{userinfo.user_name}", "{userinfo.user_password}"}

# Pre‑compiled regex to find all { ... } placeholders
_PLACEHOLDER_RE = re.compile(r"{[^{}]*}")

def format_string(string: str) -> str:
    """
    Format *string* using the global ``CURRENT_USER`` instance.
    
    The function only allows placeholders that refer to
    ``userinfo.user_name`` or ``userinfo.user_password``.  Any other
    placeholder will cause a :class:`ValueError` to be raised.
    
    Parameters
    ----------
    string : str
        The input format string.  It may contain zero or more
        ``{userinfo.user_name}`` and/or ``{userinfo.user_password}``
        placeholders.
    
    Returns
    -------
    str
        The formatted string with user information substituted in.
    
    Raises
    ------
    ValueError
        If the string contains an unsupported placeholder or if a
        formatting error occurs.
    """
    # Find all placeholders in the string
    for match in _PLACEHOLDER_RE.finditer(string):
        placeholder = match.group()
        if placeholder not in _ALLOWED_PLACEHOLDERS:
            raise ValueError(f"Unsupported placeholder: {placeholder!r}")

    try:
        # Perform the formatting with the global user instance
        return string.format(userinfo=CURRENT_USER)
    except Exception as exc:
        # Wrap any formatting exception into a ValueError
        raise ValueError(f"Formatting error: {exc}") from exc