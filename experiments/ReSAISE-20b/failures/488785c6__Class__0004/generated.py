import re

def add_safe_header(custom_value: str) -> str:
    """
    Construct a safe HTTP header string with the given user-supplied value.
    
    The function sanitizes `custom_value` by removing any CR or LF characters
    that could terminate the header prematurely and by ensuring only printable
    ASCII characters (except for control characters) remain. This mitigates
    CWE‑74: injection via header values.
    
    Parameters
    ----------
    custom_value : str
        The user-provided value for the header.
    
    Returns
    -------
    str
        A complete header line, e.g. "X-Custom: sanitized_value".
    
    Raises
    ------
    re.error
        If an invalid regular expression is used (unlikely here, but the
        function may indirectly raise it if the pattern is modified).
    """
    
    # Remove any CR or LF characters to prevent header injection.
    # Also strip leading/trailing whitespace for cleanliness.
    sanitized = re.sub(r'[\r\n]+', '', custom_value).strip()
    
    # Ensure only printable ASCII characters (0x20–0x7E) remain.
    # Non-printable or non-ASCII characters are replaced with a safe placeholder.
    sanitized = re.sub(r'[^\x20-\x7E]', '', sanitized)
    
    # If the value becomes empty, use a default safe string.
    if not sanitized:
        sanitized = "default"
    
    return f"X-Custom: {sanitized}"