import re

# Regular expression to validate a safe HTTP header value.
# Allows printable ASCII characters except CR (0x0D) and LF (0x0A).
# The pattern ensures the value does not contain any line breaks or
# control characters that could be used for CRLF injection.
SAFE_HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E]*$')

def append_user_header(user_header: str) -> str:
    """
    Append a custom header to an HTTP response.

    The function validates the supplied `user_header` value to prevent
    CRLF injection or other malformed header values.  The header name is
    fixed to ``X-Custom-Header`` to avoid header name injection.

    Args:
        user_header: The custom header value supplied by the user.

    Returns:
        A string containing the full HTTP header line, e.g.
        "X-Custom-Header: Some value".

    Raises:
        ValueError: If the header value contains disallowed characters.
    """
    if not isinstance(user_header, str):
        raise ValueError("Header value must be a string")

    # Strip any leading/trailing whitespace to avoid accidental injection.
    stripped = user_header.strip()

    if not SAFE_HEADER_VALUE_RE.fullmatch(stripped):
        raise ValueError("Header value contains disallowed characters")

    return f"X-Custom-Header: {stripped}"