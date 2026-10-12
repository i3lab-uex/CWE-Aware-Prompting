import re

def detect_js_scheme(url_string: str) -> bool:
    """
    Detect whether a string contains a potentially harmful URL scheme
    such as javascript: or vbscript:, while ignoring safe image data URLs.

    Parameters
    ----------
    url_string : str
        The string to examine for possible dangerous URL schemes.

    Returns
    -------
    bool
        True if the string involves a potentially harmful URL scheme,
        False otherwise.
    """
    if not isinstance(url_string, str):
        return False

    # Strip leading whitespace and convert to lowercase for case‑insensitive check
    stripped = url_string.lstrip().lower()

    # Directly flagged dangerous schemes
    if stripped.startswith("javascript:") or stripped.startswith("vbscript:"):
        return True

    # Handle data URLs
    if stripped.startswith("data:"):
        # Only allow image/* data URLs as safe
        # Example of a safe URL: data:image/png;base64,...
        image_pattern = re.compile(r"^data\s*:\s*image\/[a-z0-9\-\+\.]+", re.IGNORECASE)
        if image_pattern.match(stripped):
            return False
        # Any other data: scheme is considered dangerous
        return True

    return False