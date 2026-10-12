import re

def inject_custom_header(header_content: str) -> str:
    """
    Insert a user‑supplied value as a custom header in the HTTP response headers.
    
    The function sanitizes the supplied header content to prevent CRLF injection
    and other malformed header issues. It removes any carriage‑return or line‑feed
    characters, strips leading/trailing whitespace, and truncates the value to a
    safe maximum length. The resulting header is returned as a single string.
    
    Parameters
    ----------
    header_content : str
        The user‑provided custom header value.
    
    Returns
    -------
    str
        A well‑formed header line, e.g. "X-Custom-Header: sanitized_value".
    
    Notes
    -----
    - The function does not raise exceptions for malformed input; any regex errors
      will propagate normally.
    - The sanitized value is limited to 8192 characters, a common safe limit for
      HTTP header values.
    """
    
    # Maximum allowed length for a header value (RFC‑7230 suggests 8K bytes is safe)
    MAX_HEADER_LENGTH = 8192
    
    # Remove CR and LF characters to prevent header injection
    sanitized = re.sub(r'[\r\n]', '', header_content)
    
    # Strip leading/trailing whitespace
    sanitized = sanitized.strip()
    
    # Truncate to the maximum safe length
    if len(sanitized) > MAX_HEADER_LENGTH:
        sanitized = sanitized[:MAX_HEADER_LENGTH]
    
    # Return the final header string
    return f"X-Custom-Header: {sanitized}"