import re

# Regular expression that matches a valid HTTP header value.
# It must not contain CR or LF characters and should be a non‑empty string.
_VALID_HEADER_RE = re.compile(r'^[^\r\n]+$')

def append_user_header(user_header: str) -> str:
    """
    Create a custom HTTP header string from the supplied user value.

    The function validates that `user_header` does not contain carriage
    return or line feed characters, which would break the HTTP protocol.
    If the value is invalid a ValueError is raised.

    Parameters
    ----------
    user_header : str
        The custom header value supplied by the user.

    Returns
    -------
    str
        A fully‑formed HTTP header line, e.g.
        "X-Custom-Header: <user_header>".

    Raises
    ------
    ValueError
        If the supplied header value contains illegal characters.
    """
    if not isinstance(user_header, str):
        raise TypeError("user_header must be a string")

    # Validate the header value
    if not _VALID_HEADER_RE.match(user_header):
        raise ValueError(
            "Invalid header value: must not contain CR or LF characters"
        )

    # Construct the header line.  Use a standard custom header name.
    return f"X-Custom-Header: {user_header}"