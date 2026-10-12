import re

# Allowed characters for HTTP header values (token or quoted-string)
# For simplicity, we allow printable ASCII excluding control chars and CR/LF.
_ALLOWED_CHARS_RE = re.compile(r'[^\x20-\x7E]')

def _sanitize_header_value(value: str) -> str:
    """
    Remove any control characters or CR/LF that could break the header format.
    Additionally, collapse multiple spaces to a single space and strip surrounding
    whitespace.
    """
    # Remove CR, LF, and other control characters
    cleaned = _ALLOWED_CHARS_RE.sub('', value)
    # Collapse multiple spaces/tabs into a single space
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()

def insert_header_with_sanitization(custom_header_value: str) -> str:
    """
    Return a header string "X-Custom-Header: <sanitized_value>".
    
    Parameters
    ----------
    custom_header_value : str
        User supplied header value.

    Returns
    -------
    str
        Sanitized header line ready for inclusion in an HTTP response.
    
    Notes
    -----
    The function removes CR/LF and other control characters to prevent header
    injection attacks. It also normalizes whitespace.
    """
    sanitized = _sanitize_header_value(custom_header_value)
    return f"X-Custom-Header: {sanitized}"