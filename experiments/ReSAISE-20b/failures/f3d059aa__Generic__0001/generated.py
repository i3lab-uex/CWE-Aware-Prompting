import re

# Regular expression that matches a valid HTTP header value:
# RFC 7230 allows any visible ASCII characters except control chars,
# and allows optional folding whitespace (spaces or horizontal tabs).
_HEADER_VALUE_RE = re.compile(r'^[^\x00-\x1F\x7F]*$')

def append_user_header(user_header: str) -> str:
    """
    Construct a custom HTTP header line from the user supplied value.

    The function validates that `user_header` contains only allowed
    characters for an HTTP header value (visible ASCII, no control
    characters).  If the validation passes it returns a string of the form

        X-Custom-Header: <user_header>\r\n

    which can be appended to an HTTP response header block.

    Parameters
    ----------
    user_header : str
        The custom header value supplied by the user.

    Returns
    -------
    str
        A single HTTP header line including the custom value and a CRLF.

    Raises
    ------
    ValueError
        If `user_header` contains disallowed characters.
    """
    if not isinstance(user_header, str):
        raise TypeError("user_header must be a string")

    # Strip leading/trailing whitespace to avoid accidental injection
    value = user_header.strip()

    if not _HEADER_VALUE_RE.match(value):
        raise ValueError("user_header contains invalid characters for an HTTP header value")

    # Construct the header line
    return f"X-Custom-Header: {value}\r\n"