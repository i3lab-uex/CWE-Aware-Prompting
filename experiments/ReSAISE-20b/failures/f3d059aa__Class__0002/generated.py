import re

# RFC 7230 token characters: !#$%&'*+-.^_`|~ and ASCII alphanumerics
TOKEN_RE = re.compile(r'^[!#$%&\'*+\-.^_`|~0-9a-zA-Z]+$')
# Allowed header value characters: printable ASCII excluding CR and LF
VALUE_RE = re.compile(r'^[\x20-\x7E]+$')

def append_user_header(user_header: str) -> str:
    """
    Construct a safe custom header line for inclusion in HTTP responses.

    The function validates the user supplied header value against a
    whitelist of characters permitted in HTTP headers.  If the value
    contains any disallowed characters (e.g., CR, LF, or non‑printable
    bytes) the function raises a ValueError.

    Parameters:
        user_header (str): The custom header value supplied by the user.

    Returns:
        str: A fully formed HTTP header line including CRLF terminator.
    """
    # Basic validation of the user supplied header value
    if not isinstance(user_header, str):
        raise TypeError("user_header must be a string")

    # Reject empty values – headers should have at least one character
    if not user_header:
        raise ValueError("user_header cannot be empty")

    # Ensure the value contains only allowed printable ASCII characters
    if not VALUE_RE.match(user_header):
        raise ValueError("user_header contains disallowed characters")

    # Build the header line.  The colon and space are fixed, we do not
    # allow any additional CR/LF in the value.
    header_line = f"X-Custom-Header: {user_header}\r\n"
    return header_line