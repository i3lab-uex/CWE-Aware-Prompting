import re

# Regular expression to validate that the header value contains only printable ASCII characters
# and does not include CR or LF (which would allow injection of additional headers).
HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E]*$')

def insert_custom_header(custom_header: str) -> str:
    """
    Insert a custom header into an HTTP response.

    The function validates the supplied `custom_header` value to ensure it
    does not contain any control characters that could be used for header
    injection.  The returned string is a single line containing the header
    name and value followed by CRLF, ready to be appended to an HTTP
    response.

    Args:
        custom_header: The header value supplied by the user.  It must
                       consist solely of printable ASCII characters.

    Returns:
        A string containing the full header line, e.g.
        "X-Custom-Header: <value>\r\n".

    Raises:
        ValueError: If the header value contains disallowed characters.
        re.error:   If the regular expression fails to compile (unlikely).
    """
    # Ensure the header value is a string
    if not isinstance(custom_header, str):
        raise TypeError("custom_header must be a string")

    # Validate that the header value does not contain CR or LF
    if not HEADER_VALUE_RE.fullmatch(custom_header):
        raise ValueError(
            "custom_header contains invalid characters; "
            "only printable ASCII (0x20-0x7E) are allowed"
        )

    # Construct the header line
    return f"X-Custom-Header: {custom_header}\r\n"