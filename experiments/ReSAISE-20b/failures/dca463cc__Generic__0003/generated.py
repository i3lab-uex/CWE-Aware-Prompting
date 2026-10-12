import re

# Regular expression that matches a valid HTTP header field value.
# According to RFC 7230, a header field value may contain any
# visible ASCII characters (0x21-0x7E) except for control
# characters and the following delimiters: CR, LF, ":".
HEADER_VALUE_RE = re.compile(r'^[\x21-\x7E]+$')


def insert_custom_header(custom_header: str) -> str:
    """
    Insert a custom header into the HTTP response headers.

    Parameters
    ----------
    custom_header : str
        The value of the custom header provided by the user. It must be a
        single-line string containing only printable ASCII characters,
        excluding CR, LF and the colon delimiter.

    Returns
    -------
    str
        A header line in the form "X-Custom-Header: <value>\r\n".

    Notes
    -----
    The function performs minimal validation to prevent CRLF injection.
    If the input does not match the allowed pattern, a ValueError is raised.

    Examples
    --------
    >>> insert_custom_header('MyValue')
    'X-Custom-Header: MyValue\\r\\n'
    """
    if not isinstance(custom_header, str):
        raise TypeError("custom_header must be a string")

    # Strip any surrounding whitespace to avoid accidental injection
    value = custom_header.strip()

    if not HEADER_VALUE_RE.match(value):
        raise ValueError(
            "custom_header contains invalid characters; "
            "only printable ASCII (0x21-0x7E) are allowed"
        )

    return f"X-Custom-Header: {value}\r\n"