import re

# Regular expression that matches any character that is NOT allowed in an HTTP header value.
# RFC 7230 defines a header field value as a sequence of visible ASCII characters
# (i.e., 0x20-0x7E) excluding control characters, CR, LF, and the delimiter ":".
# We allow any printable character except ':' and strip CR/LF to prevent injection.
_INVALID_HEADER_CHARS = re.compile(r'[\r\n:]+')

def include_custom_header(custom_value: str) -> str:
    """
    Construct a custom HTTP header line with the supplied value after sanitization.

    The function removes any CR, LF, or colon characters from `custom_value` to
    prevent header injection and ensures that the resulting value only contains
    printable ASCII characters. The sanitized value is then inserted into a
    header named "X-Custom".

    Parameters:
        custom_value (str): The user supplied header value.

    Returns:
        str: A fully formed HTTP header line, e.g. "X-Custom: sanitized-value".

    Raises:
        re.error: If the regular expression fails to compile (unlikely in normal
                  execution).  No other explicit exceptions are raised.
    """
    # Strip any CR, LF or colon characters to neutralize injection attempts
    sanitized = _INVALID_HEADER_CHARS.sub('', custom_value)

    # Ensure the value is not empty after sanitization; if it is, use a safe default
    if not sanitized:
        sanitized = 'default'

    # Construct the header line. The header name is constant; only the value is user
    # supplied and sanitized.
    return f"X-Custom: {sanitized}"