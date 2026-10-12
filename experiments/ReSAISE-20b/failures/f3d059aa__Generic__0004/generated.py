import re

# Regular expression to validate a header value.
# It must not contain CR or LF characters and should be ASCII printable.
_HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E]*$')

def append_user_header(user_header: str) -> str:
    """
    Append a custom header to the response headers.

    The function validates that `user_header` contains only
    printable ASCII characters (no CR or LF).  If the validation fails,
    a ValueError is raised to avoid HTTP header injection.

    Parameters
    ----------
    user_header : str
        The value of the custom header supplied by a user.

    Returns
    -------
    str
        A string containing the full HTTP header line, e.g.
        "X-Custom-Header: <value>\r\n".

    Raises
    ------
    ValueError
        If the header value contains disallowed characters.
    """
    if not isinstance(user_header, str):
        raise ValueError("Header value must be a string")

    # Reject any CR or LF characters to prevent header injection.
    if not _HEADER_VALUE_RE.match(user_header):
        raise ValueError("Header value contains invalid characters")

    # Return the header line in a format suitable for HTTP responses.
    return f"X-Custom-Header: {user_header}\r\n"