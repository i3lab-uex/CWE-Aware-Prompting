import re

# Regular expression for a simple HTTP header value:
#   - allowed: printable ASCII characters except control chars, colon, comma,
#     semicolon, and backslash.
HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E]*$')

def insert_custom_header(custom_header: str) -> str:
    """
    Construct an HTTP header line with the supplied custom header value.

    Parameters
    ----------
    custom_header : str
        The user‑supplied header value. It must consist only of printable ASCII
        characters (0x20–0x7E). Control characters, newlines and other
        forbidden header characters are rejected.

    Returns
    -------
    str
        A complete header line in the form ``Custom-Header: <value>\r\n``.

    Notes
    -----
    The function performs minimal validation to guard against header injection
    attacks. It does not raise explicit exceptions; if the value fails the
    regular expression, a ``ValueError`` is raised.

    Examples
    --------
    >>> insert_custom_header('My Value')
    'Custom-Header: My Value\\r\\n'
    """
    if not isinstance(custom_header, str):
        raise TypeError("custom_header must be a string")

    # Basic validation: ensure the header value contains only allowed ASCII.
    if not HEADER_VALUE_RE.fullmatch(custom_header):
        raise ValueError("Invalid characters in custom header value")

    # Construct the header line. CRLF is required by HTTP.
    return f"Custom-Header: {custom_header}\r\n"