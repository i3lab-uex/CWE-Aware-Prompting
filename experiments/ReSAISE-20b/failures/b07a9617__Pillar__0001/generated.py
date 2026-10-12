import re

def insert_header_with_sanitization(custom_header_value: str) -> str:
    """
    Insert a user-supplied value as a custom header in the HTTP response.
    
    The function sanitizes the input to prevent header injection and
    other CWE-707 related issues by removing control characters,
    CR/LF sequences, and non‑printable characters. Only a safe subset
    of printable ASCII is retained.
    
    Parameters
    ----------
    custom_header_value : str
        The user‑supplied header value.

    Returns
    -------
    str
        A string containing the full HTTP header line, e.g.
        "X-Custom-Header: sanitized_value".
    """
    
    # Remove any CR or LF characters that could terminate the header line
    sanitized = re.sub(r'[\r\n]+', '', custom_header_value)

    # Strip leading/trailing whitespace
    sanitized = sanitized.strip()

    # Allow only printable ASCII characters (32-126). Remove anything else.
    sanitized = re.sub(r'[^\x20-\x7E]', '', sanitized)

    # If the result is empty, use a placeholder to avoid sending an empty header
    if not sanitized:
        sanitized = 'unknown'

    return f"X-Custom-Header: {sanitized}"