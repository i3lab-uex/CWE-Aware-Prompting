import re

# Regular expression that matches characters allowed in HTTP header values.
# According to RFC 7230, header field-values may contain any visible ASCII
# characters except for control chars (0x00–0x1F and 0x7F). We also reject
# CR (0x0D) and LF (0x0A) to prevent header injection.
_HEADER_SAFE_RE = re.compile(r'[\x20-\x7E]')

def _sanitize_header_value(value: str) -> str:
    """
    Remove any characters that are not allowed in an HTTP header value.
    This prevents CRLF injection and ensures the resulting string is a
    single line of visible ASCII characters.

    Parameters:
        value (str): The raw user-provided header value.

    Returns:
        str: A sanitized string containing only allowed characters.
    """
    # Keep only the matched safe characters
    return ''.join(_HEADER_SAFE_RE.findall(value))

def insert_custom_header(user_header: str) -> str:
    """
    Insert a custom header into an HTTP response.

    The function sanitizes the user-provided header value to avoid
    injection attacks. It returns a string that can be appended to the
    response headers.

    Parameters:
        user_header (str): The value supplied by the user for the custom
                           header.

    Returns:
        str: A complete HTTP header line, e.g.
             "X-Custom-Header: sanitized_value\r\n".
    """
    # Sanitize the user input
    safe_value = _sanitize_header_value(user_header)

    # Construct the header line. Using a fixed header name to avoid
    # header confusion; only the value is user-controlled.
    return f"X-Custom-Header: {safe_value}\r\n"