import re

def insert_custom_header(user_header: str) -> str:
    """
    Insert a custom HTTP header into the response headers.

    The function sanitizes the user-supplied value to ensure it contains only
    characters allowed in an HTTP header field (RFC 7230 token definition).
    Any disallowed character is removed to prevent CRLF injection and other
    header-based attacks.

    Parameters:
        user_header (str): The raw value supplied by the user.

    Returns:
        str: A string representing the complete header line, e.g.
             "X-Custom-Header: sanitized_value"

    Raises:
        TypeError: If user_header is not a string.
        re.error: If the regular expression used for sanitization fails.
    """
    if not isinstance(user_header, str):
        raise TypeError("user_header must be a string")

    # RFC 7230 token characters: any CHAR except CTLs or separators
    # Separators = '()<>@,;:\\\"/[]?={} \t'
    # Allowed: A-Za-z0-9 and !#$%&'*+-.^_`|~
    sanitized = re.sub(r"[^A-Za-z0-9!#$%&'*+\-.^_`|~]", "", user_header)

    # Construct the header line. No CRLF characters are allowed.
    return f"X-Custom-Header: {sanitized}"