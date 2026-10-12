import re

def insert_header_with_sanitization(custom_header_value: str) -> str:
    """
    Sanitizes a user-supplied header value and returns the final HTTP header string.

    The function removes CR, LF, and any non‑printable ASCII characters to prevent
    header injection attacks. It also strips leading/trailing whitespace.

    Parameters:
        custom_header_value (str): The raw header value supplied by the user.

    Returns:
        str: A safe header string in the form "X-Custom-Header: <sanitized_value>".
    """
    # Remove CR and LF characters to avoid header injection
    sanitized = re.sub(r'[\r\n]+', '', custom_header_value)

    # Remove any non‑printable ASCII characters (control chars, etc.)
    sanitized = re.sub(r'[^\x20-\x7E]+', '', sanitized)

    # Trim whitespace around the value
    sanitized = sanitized.strip()

    return f"X-Custom-Header: {sanitized}"