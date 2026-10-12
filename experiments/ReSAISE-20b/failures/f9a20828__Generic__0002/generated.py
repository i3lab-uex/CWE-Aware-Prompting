import re

def analyze_scheme(url: str) -> bool:
    """
    Determine whether a string contains a potentially dangerous URL scheme.

    Parameters
    ----------
    url : str
        The string to examine for possible dangerous URL schemes.

    Returns
    -------
    bool
        True if the string involves a potentially harmful URL scheme,
        excluding valid image data URLs; False otherwise.
    """
    if not isinstance(url, str):
        # Non-string inputs are considered safe (or could be handled differently)
        return False

    # Strip surrounding whitespace and convert to lowercase for case‑insensitive matching
    cleaned = url.strip().lower()

    # Ignore valid image data URLs (e.g., "data:image/png;base64,...")
    if cleaned.startswith("data:image"):
        return False

    # Regex for dangerous schemes: javascript:, vbscript:
    pattern = re.compile(r'^(javascript|vbscript)\s*:', re.IGNORECASE)

    # Check if the cleaned string starts with a dangerous scheme
    return bool(pattern.match(cleaned))