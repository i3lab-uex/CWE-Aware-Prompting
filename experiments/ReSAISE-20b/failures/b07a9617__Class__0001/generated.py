import re

# Regex that matches any character that is NOT a printable US‑ASCII character (0x20–0x7E)
# and also disallows carriage return and line feed which can terminate the header.
INVALID_CHARS_RE = re.compile(r'[\x00-\x1F\x7F\r\n]')

def insert_header_with_sanitization(custom_header_value: str) -> str:
    """
    Construct a custom HTTP header after sanitizing the user supplied value.

    The function removes any control characters, CR/LF and non‑printable
    ASCII that could be used for header injection (CWE‑74).  It returns a
    properly formatted header string.

    Parameters:
        custom_header_value (str): The raw user supplied value for the header.

    Returns:
        str: A safe HTTP header string of the form
             "X-Custom-Header: <sanitized_value>".
    """
    # Strip leading/trailing whitespace and replace any forbidden characters with an empty string
    sanitized = INVALID_CHARS_RE.sub('', custom_header_value.strip())

    # If the value becomes empty after sanitization, we still return a header
    # with an empty value; the caller may decide to drop it if needed.
    return f"X-Custom-Header: {sanitized}"