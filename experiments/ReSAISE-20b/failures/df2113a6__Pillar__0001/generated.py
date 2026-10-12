import re

def insert_custom_header(user_header: str) -> str:
    """
    Insert a custom HTTP header with the given user-supplied value.
    
    The function sanitizes the input to ensure it cannot break out of the
    header field or introduce CRLF injection.  It removes any carriage return,
    line feed, and other control characters that could be interpreted as
    header delimiters.  The sanitized value is then inserted into a standard
    header line.

    Args:
        user_header: The raw string supplied by the user for the custom
            header value.

    Returns:
        A full HTTP header line string containing the sanitized user value.
    
    Raises:
        re.error: If the regular expression used for sanitization fails
            (unlikely, but possible with malformed patterns).
    """
    # Remove CRLF and other control characters that could break the header.
    # The pattern matches any character with ASCII code <= 31 or == 127.
    sanitized = re.sub(r'[\x00-\x1F\x7F]+', '', user_header)
    
    # Build the header line. Use a fixed, safe header name.
    return f"X-Custom-Header: {sanitized}"