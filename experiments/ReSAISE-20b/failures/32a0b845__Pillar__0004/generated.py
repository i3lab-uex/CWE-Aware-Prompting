import re

def add_customized_header(header_content: str) -> str:
    """
    Insert a custom header into an HTTP response, sanitizing the user-provided
    value to prevent injection or malformed headers.

    The function removes any non-printable characters (control codes,
    tabs, newlines, etc.) from the supplied header content. Only visible
    ASCII characters (code points 32-126) are retained, which is a safe
    subset for HTTP header field values.

    Args:
        header_content: User-supplied string to be used as the header value.

    Returns:
        A full HTTP header line including the custom header name and a
        CRLF terminator.

    Raises:
        re.error: If the regular expression fails to compile (unlikely).
    """
    # Keep only printable ASCII characters 0x20-0x7E
    sanitized = re.sub(r'[^\x20-\x7E]', '', header_content)
    return f"X-Custom-Header: {sanitized}\r\n"