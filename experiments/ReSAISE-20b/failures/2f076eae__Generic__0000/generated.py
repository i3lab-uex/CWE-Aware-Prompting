import re

# Regular expression that matches a valid HTTP header value.
# According to RFC 7230, header values must be made of printable ASCII
# characters (decimal 32-126) and cannot contain CR or LF.
_HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E]*$')

def add_response_header(response_header: str) -> str:
    """
    Insert a custom header into the response headers.

    Parameters
    ----------
    response_header : str
        The value supplied by the user for the custom header.  It must be a
        valid HTTP header value, i.e. consist only of printable ASCII
        characters (space through tilde) and must not contain CR or LF.

    Returns
    -------
    str
        The full header line ready to be appended to an HTTP response,
        e.g. ``"X-Custom-Header: <value>"``.

    Notes
    -----
    The function does not raise a custom exception; instead it will raise
    ``re.error`` if the regular expression is somehow malformed (unlikely),
    or ``ValueError`` if the supplied header value fails validation.
    """
    # Validate that the header value contains only allowed characters
    if not _HEADER_VALUE_RE.match(response_header):
        raise ValueError(
            "Invalid header value: must contain only printable ASCII characters "
            "(space through tilde) and cannot include CR or LF."
        )

    # Construct the header line
    return f"X-Custom-Header: {response_header}"