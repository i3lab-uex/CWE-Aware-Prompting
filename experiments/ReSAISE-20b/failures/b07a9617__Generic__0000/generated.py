import re

def insert_header_with_sanitization(custom_header_value: str) -> str:
    """
    Return a single HTTP header line containing the user‑supplied value
    after sanitizing it to prevent injection of CRLF or other control
    characters that could break the HTTP protocol or cause security issues.

    Parameters:
        custom_header_value (str): The raw value supplied by the user.

    Returns:
        str: A header line in the form 'X-Custom-Header: <sanitized_value>'.

    Notes:
        * All CR (`\r`) and LF (`\n`) characters are removed.
        * Any other control character (0x00–0x1F and 0x7F) is stripped.
        * Leading/trailing whitespace is trimmed, and internal
          sequences of whitespace are collapsed to a single space.
    """
    # Remove CRLF characters that could break the header line
    sanitized = custom_header_value.replace('\r', '').replace('\n', '')

    # Remove all remaining control characters (0x00–0x1F, 0x7F)
    sanitized = re.sub(r'[\x00-\x1f\x7f]', '', sanitized)

    # Collapse internal whitespace and trim edges
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()

    # If the value is empty after sanitization, use a safe default
    if not sanitized:
        sanitized = 'default'

    return f"X-Custom-Header: {sanitized}"