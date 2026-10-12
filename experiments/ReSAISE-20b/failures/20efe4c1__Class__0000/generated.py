import re

def verify_javascript_protocol(url_input: str) -> bool:
    """
    Detect whether the supplied string contains a potentially dangerous URL
    scheme such as `javascript:` or `vbscript:`, while ignoring valid image
    data URLs.

    Parameters
    ----------
    url_input : str
        The URL string to be examined.

    Returns
    -------
    bool
        True if a harmful scheme is present, False otherwise.
    """
    # Ensure the input is a string
    if not isinstance(url_input, str):
        return False

    # Strip leading/trailing whitespace for accurate detection
    stripped = url_input.strip()

    # Ignore data URLs that point to images (e.g., data:image/png;base64,...)
    if stripped.lower().startswith("data:image"):
        return False

    # Regex to match dangerous schemes: javascript, vbscript
    # We allow optional whitespace before the colon and case‑insensitive matching.
    dangerous_pattern = re.compile(r"^(?P<scheme>javascript|vbscript)\s*:", re.I)

    return bool(dangerous_pattern.match(stripped))