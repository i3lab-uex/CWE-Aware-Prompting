import re

# Allowed characters for HTTP header values according to RFC 7230:
# any printable US-ASCII character except control characters and
# the separator characters: ()<>@,;:\"/[]?={} \t
HEADER_VALUE_RE = re.compile(r'^[\x21-\x7E]*$')

def append_user_header(user_header: str) -> str:
    """
    Validate a user supplied header value and return it as an HTTP header line.
    
    Parameters
    ----------
    user_header : str
        The raw value supplied by the user.
    
    Returns
    -------
    str
        A complete header string in the form 'X-User-Header: <value>\r\n'.
    
    Raises
    ------
    ValueError
        If the supplied header value contains characters that are not permitted in
        an HTTP header value.
    """
    # Ensure the input is a string (Python 3 only)
    if not isinstance(user_header, str):
        raise ValueError("Header value must be a string")

    # Strip surrounding whitespace to avoid accidental injection of CRLF
    stripped = user_header.strip()

    # Validate the header value against the allowed character set
    if not HEADER_VALUE_RE.match(stripped):
        raise ValueError("Header value contains invalid characters")

    # Construct the header line safely
    return f"X-User-Header: {stripped}\r\n"