import re

def has_dangerous_scheme(uri_str: str) -> bool:
    """
    Detects whether a URI contains a potentially dangerous scheme
    (e.g., javascript:, vbscript:) while ignoring safe image data URLs.

    Parameters
    ----------
    uri_str : str
        The URI string to examine.

    Returns
    -------
    bool
        True if a dangerous scheme is present; False otherwise.
    """
    # Strip leading whitespace for robustness
    trimmed = uri_str.lstrip()

    # Regex to capture the scheme (letters, digits, '+', '-', '.') before a colon
    scheme_match = re.match(r'^([a-z][a-z0-9+.-]*)\s*:', trimmed, re.IGNORECASE)
    if not scheme_match:
        return False  # No scheme present

    scheme = scheme_match.group(1).lower()

    # Dangerous schemes to block
    dangerous_schemes = {
        'javascript',
        'vbscript',
        'data',      # data: URIs are dangerous unless they are image/* types
    }

    if scheme not in dangerous_schemes:
        return False

    # If the scheme is 'data', allow only image/* MIME types
    if scheme == 'data':
        # Extract the MIME type part before ';' or ','
        data_part = trimmed[5:]  # strip 'data:'
        mime_type = data_part.split(';', 1)[0].split(',', 1)[0]
        if mime_type.startswith('image/'):
            return False
        # Any other data: scheme is considered dangerous
    return True