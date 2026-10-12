import re

# Regex pattern that matches any character that is NOT a valid HTTP header field value.
# RFC 7230 specifies that field values must be visible ASCII (octets 32-126) except for
# CR and LF. We therefore allow characters in the range 0x20-0x7E.
# Any other character (including newlines, tabs, non‑ASCII) will be removed.
_INVALID_HEADER_CHAR_RE = re.compile(r'[^\x20-\x7E]')

def insert_custom_header(user_header: str) -> str:
    """
    Insert a custom header into an HTTP response. The supplied user_header value
    is sanitized to ensure it contains only printable ASCII characters (0x20–0x7E).
    This prevents injection of CRLF sequences or other control characters that
    could break the HTTP protocol or enable response‑splitting attacks.

    Parameters:
        user_header (str): The raw header value supplied by the user.

    Returns:
        str: A single header line suitable for inclusion in an HTTP response,
             e.g. "X-Custom-Header: sanitized_value\r\n".
    """
    # Strip any invalid characters from the user input.
    sanitized = _INVALID_HEADER_CHAR_RE.sub('', user_header)

    # Construct the header line. Use a hard‑coded header name to avoid
    # allowing arbitrary header names from the user.
    header_line = f"X-Custom-Header: {sanitized}\r\n"
    return header_line