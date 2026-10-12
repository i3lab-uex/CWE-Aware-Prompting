import re

# Regular expression to validate a header value.
# RFC 7230 defines a "token" as any combination of characters
# except separators and control characters.  For simplicity we
# allow printable ASCII excluding colon, comma, and whitespace.
HEADER_VALUE_RE = re.compile(r'^[\x21-\x2B\x2D-\x3A\x3C-\x5B\x5D-\x7E]+$')

def add_custom_header(header_value: str) -> str:
    """
    Return a complete HTTP header line containing the custom header
    with the supplied value.

    Parameters
    ----------
    header_value : str
        The user-supplied header value.  It must match the pattern
        defined by HEADER_VALUE_RE, otherwise a ValueError is raised.

    Returns
    -------
    str
        The full header line, e.g. "X-Custom-Header: myvalue\r\n".

    Raises
    ------
    ValueError
        If `header_value` contains characters that are not allowed in a
        header value according to the RFC 7230 token definition.
    """
    if not isinstance(header_value, str):
        raise ValueError("header_value must be a string")

    # Ensure the header value is safe and well‑formed.
    if not HEADER_VALUE_RE.match(header_value):
        raise ValueError(
            "header_value contains invalid characters; "
            "only printable ASCII tokens are allowed"
        )

    # Construct the header line.  Use CRLF as per RFC 7230.
    return f"X-Custom-Header: {header_value}\r\n"