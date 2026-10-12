import re

# Regular expression that matches a string containing only printable ASCII characters
# (space through tilde) and excludes control characters, CR, LF, etc.
_PRINTABLE_ASCII_RE = re.compile(r'^[\x20-\x7E]+$')

def insert_custom_header(custom_header: str) -> str:
    """
    Build a single HTTP header line for the custom header value.

    The function validates that the provided header value consists only of
    printable ASCII characters (space to tilde).  This prevents CRLF injection,
    header splitting, and other malformed-header attacks.

    Args:
        custom_header: The user‑supplied header value.  Must be a string.

    Returns:
        A properly formatted header line, e.g.
            "X-Custom-Header: some_value\r\n"

    Raises:
        ValueError: If the header value contains disallowed characters.
    """
    if not isinstance(custom_header, str):
        raise TypeError("custom_header must be a string")

    # Ensure the value is non‑empty and contains only allowed characters
    if not custom_header:
        raise ValueError("custom_header cannot be empty")

    if not _PRINTABLE_ASCII_RE.fullmatch(custom_header):
        raise ValueError(
            "custom_header contains invalid characters; "
            "only printable ASCII (space to tilde) are allowed"
        )

    # Construct the header line with CRLF as per HTTP specifications
    return f"X-Custom-Header: {custom_header}\r\n"