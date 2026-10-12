import re

# Allowed characters for a simple HTTP header value:
# Visible ASCII characters (0x21–0x7E) and spaces.
_HEADER_VALUE_RE = re.compile(r'^[\x20\x21-\x7E]*$')


def append_user_header(user_header: str) -> str:
    """
    Append a custom header to an HTTP response.

    The function validates the supplied `user_header` value against
    a simple regular expression that permits only visible ASCII
    characters and spaces.  This prevents header injection attacks
    such as CRLF injection.

    Parameters
    ----------
    user_header : str
        The custom header value provided by the user.

    Returns
    -------
    str
        A single header line in the form:
            "X-Custom-Header: <user_header>"

    Raises
    ------
    ValueError
        If `user_header` contains characters that are not allowed.
    """
    if not isinstance(user_header, str):
        raise TypeError("user_header must be a string")

    if not _HEADER_VALUE_RE.match(user_header):
        raise ValueError(
            "Invalid header value: only visible ASCII characters and spaces are allowed"
        )

    return f"X-Custom-Header: {user_header}"