import re

def detect_malicious_url_scheme(url_string: str) -> bool:
    """
    Detects potentially malicious URL schemes such as javascript:, vbscript:,
    while ignoring safe image data URLs (e.g., data:image/...).

    Parameters
    ----------
    url_string : str
        The URL string to inspect.

    Returns
    -------
    bool
        True if a dangerous scheme is detected, False otherwise.
    """
    if not isinstance(url_string, str):
        return False

    # Strip leading/trailing whitespace
    trimmed = url_string.strip()

    # Ignore safe image data URLs
    if trimmed.lower().startswith("data:image/"):
        return False

    # Regex for dangerous schemes at the start of the string
    dangerous_pattern = re.compile(r'^(?i)(javascript|vbscript):')
    return bool(dangerous_pattern.match(trimmed))