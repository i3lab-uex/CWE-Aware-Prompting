import re

def detect_malicious_url_scheme(url_string: str) -> bool:
    """
    Detects whether the supplied string contains a potentially malicious URL scheme
    such as `javascript:` or `vbscript:` while ignoring valid image data URLs.

    Parameters
    ----------
    url_string : str
        The string to inspect for dangerous URL schemes.

    Returns
    -------
    bool
        True if a dangerous scheme is detected, False otherwise.
    """
    if not isinstance(url_string, str):
        return False

    # Strip leading/trailing whitespace for robust matching
    stripped = url_string.strip()

    # Quick check: ignore valid image data URLs entirely
    if re.match(r'(?i)^data:image/', stripped):
        return False

    # Pattern matches dangerous schemes at the start of the string.
    # It allows optional whitespace, case-insensitive matching,
    # and expects a colon, semicolon or whitespace after the scheme.
    dangerous_pattern = re.compile(r'(?i)^\s*(javascript|vbscript)(?::|\s)', flags=re.IGNORECASE)

    return bool(dangerous_pattern.search(stripped))