import re

def detect_js_scheme(url_string: str) -> bool:
    """
    Detects potentially dangerous URL schemes such as `javascript:` or
    `vbscript:`, while ignoring safe image data URLs (e.g. `data:image/png;base64,...`).

    Parameters
    ----------
    url_string : str
        The URL string to examine.

    Returns
    -------
    bool
        ``True`` if the string contains a dangerous scheme, otherwise ``False``.

    Notes
    -----
    * Leading/trailing whitespace is ignored.
    * The scheme comparison is case‑insensitive.
    * Only the scheme part (before the first colon) is considered for detection.
    """
    if not isinstance(url_string, str):
        return False

    # Strip whitespace and convert to lower case for comparison
    trimmed = url_string.strip().lower()

    # If the string does not contain a colon, it cannot have a scheme
    if ':' not in trimmed:
        return False

    # Extract the part before the first colon (the scheme)
    scheme = trimmed.split(':', 1)[0]

    # Dangerous schemes that we want to flag
    dangerous_schemes = {'javascript', 'vbscript'}

    if scheme in dangerous_schemes:
        return True

    # Handle data URLs: allow only image types
    if scheme == 'data':
        # Check the MIME type before the first semicolon or comma
        mime_part = trimmed[5:].split(';', 1)[0].split(',', 1)[0]
        # Allow only image/* MIME types
        if not mime_part.startswith('image/'):
            return True

    return False