import re

# RFC 7230 token characters: any CHAR except CTLs or separators
_TOKEN_RE = re.compile(r"^[!#$%&'*+\-.^_`|~0-9a-zA-Z]+$")

def insert_custom_header(custom_header: str) -> str:
    """
    Construct a safe HTTP header line containing the user supplied
    value for `X-Custom-Header`.  The function validates that the
    header value consists only of allowed token characters to avoid
    CRLF injection and other header injection attacks.

    Parameters
    ----------
    custom_header : str
        The user supplied header value.  It must match the token pattern.

    Returns
    -------
    str
        A complete header line, e.g. 'X-Custom-Header: value\r\n'.

    Raises
    ------
    ValueError
        If the header value contains disallowed characters.
    """
    if not isinstance(custom_header, str):
        raise ValueError("custom_header must be a string")

    # Strip surrounding whitespace; empty values are allowed but
    # still validated.
    value = custom_header.strip()

    if not _TOKEN_RE.match(value):
        raise ValueError(
            "Invalid header value: must contain only token characters "
            "(letters, digits, and !#$%&'*+-.^_`|~)"
        )

    # Construct the header line safely.  CRLF is added explicitly.
    return f"X-Custom-Header: {value}\r\n"