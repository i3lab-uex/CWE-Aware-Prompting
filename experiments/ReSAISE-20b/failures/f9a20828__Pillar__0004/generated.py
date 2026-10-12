import re

def analyze_scheme(url: str) -> bool:
    """
    Detects potentially harmful URL schemes in a string, ignoring valid image data URLs.

    Parameters
    ----------
    url : str
        The URL string to examine.

    Returns
    -------
    bool
        True if the string contains a dangerous scheme (e.g., javascript, vbscript,
        or non‑image data URLs); False otherwise.
    """
    if not isinstance(url, str):
        # Non‑string inputs are considered unsafe by default.
        return True

    # Strip leading whitespace for robust detection
    trimmed = url.lstrip()

    # Check for common dangerous schemes (case‑insensitive)
    if re.match(r'^(javascript|vbscript)\b', trimmed, re.IGNORECASE):
        return True

    # Detect data URLs that are not image types
    if trimmed.lower().startswith('data:'):
        # Allow only data:image/... URLs
        if not re.match(r'^data:image/', trimmed, re.IGNORECASE):
            return True

    # No dangerous scheme detected
    return False