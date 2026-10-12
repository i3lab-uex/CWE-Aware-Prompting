import re

def insert_header_with_sanitization(custom_header_value: str) -> str:
    """
    Insert a user‑supplied value as a custom header in an HTTP response.
    
    The function sanitizes the input by:
        * Removing CR and LF characters to prevent header injection.
        * Stripping leading/trailing whitespace.
        * Removing any non‑printable ASCII characters (except tab).
    
    Parameters
    ----------
    custom_header_value : str
        The user‑provided header value.

    Returns
    -------
    str
        A single HTTP header line with the sanitized value.
    
    Notes
    -----
    The function does not raise custom exceptions; any regex errors will propagate.
    """
    # Remove CR and LF to avoid header injection
    sanitized = re.sub(r'[\r\n]', '', custom_header_value)

    # Strip whitespace around the value
    sanitized = sanitized.strip()

    # Remove any non‑printable ASCII characters except tab (0x09)
    sanitized = re.sub(r'[^\x20-\x7E\x09]', '', sanitized)

    # Construct the header line
    return f"X-Custom-Header: {sanitized}"