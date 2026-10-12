import re

def is_javascript_scheme(s: str) -> bool:
    """
    Detects if a string contains a potentially malicious URL scheme
    (e.g., javascript:, jscript:, vbscript:) while ignoring image data URLs.

    Parameters
    ----------
    s : str
        The string to examine.

    Returns
    -------
    bool
        True if the string contains a malicious scheme (excluding image data URLs),
        False otherwise.
    """
    # Normalise to lower case for case‑insensitive matching
    lowered = s.lower()

    # Check for explicit malicious schemes at the start of the string
    if re.match(r'^\s*(javascript|jscript|vbscript)\b', lowered):
        return True

    # Detect data URLs
    if re.match(r'^\s*data:', lowered):
        # Ignore image data URLs (e.g., data:image/png;base64,...)
        if re.match(r'^\s*data:image\b', lowered):
            return False
        # Other data URLs are considered suspicious
        return True

    # No malicious scheme detected
    return False