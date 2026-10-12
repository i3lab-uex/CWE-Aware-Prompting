import re

# RFC 7230 token characters (ASCII letters, digits, and these punctuation marks)
_TOKEN_RE = re.compile(r"^[A-Za-z0-9!#$%&'*+\-.^_`|~]+$")

def insert_custom_header(user_header: str) -> str:
    """
    Insert a custom header into an HTTP response.

    Parameters
    ----------
    user_header : str
        The value supplied by the user for the custom header.

    Returns
    -------
    str
        A string containing a properly formatted HTTP header line, e.g.
        "X-Custom-Header: value\r\n".

    Raises
    ------
    ValueError
        If the supplied header value contains characters not allowed in an HTTP
        token, to prevent injection or malformed headers.
    """
    if not isinstance(user_header, str):
        raise ValueError("Header value must be a string")

    # Validate the header value against allowed token characters.
    if not _TOKEN_RE.fullmatch(user_header):
        raise ValueError(
            "Header value contains invalid characters. "
            "Only token characters are allowed."
        )

    # Construct the header line.
    return f"X-Custom-Header: {user_header}\r\n"