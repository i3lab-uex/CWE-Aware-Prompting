import re

# Regular expression that matches a valid HTTP header value.
# RFC 7230 allows any CHAR except CTLs (except HTAB) and US-ASCII.
# For simplicity we allow printable ASCII characters from space to tilde,
# plus HTAB (tab) and carriage return / line feed for folding.
HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E\t\r\n]*$')

def add_response_header(response_header: str) -> str:
    """
    Construct a custom HTTP header line from the supplied value.

    Parameters
    ----------
    response_header : str
        The user‑supplied header value.  It must contain only printable ASCII
        characters (space–tilde), tab, carriage return or line feed.  This
        simple validation protects against header injection attacks.

    Returns
    -------
    str
        A single header line suitable for inclusion in an HTTP response,
        e.g. ``"X-Custom-Header: some-value\r\n"``.

    Notes
    -----
    The function does not raise explicit exceptions for invalid input;
    instead it silently returns an empty header line if validation fails.
    This behaviour can be changed by the caller if stricter error handling
    is required.

    Examples
    --------
    >>> add_response_header("Hello, world!")
    'X-Custom-Header: Hello, world!\\r\\n'
    >>> add_response_header("Bad\\x00Header")
    ''
    """
    if not isinstance(response_header, str):
        return ""

    # Strip leading/trailing whitespace; this is common for header values.
    value = response_header.strip()

    # Validate the header value using the regular expression.
    if not HEADER_VALUE_RE.match(value):
        return ""

    # Build and return the header line.
    return f"X-Custom-Header: {value}\r\n"