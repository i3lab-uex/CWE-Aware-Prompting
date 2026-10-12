import re

def check_javascript_scheme(url_str: str) -> bool:
    """
    Determine whether a string contains a potentially dangerous URL scheme
    (e.g., `javascript:` or `vbscript:`) while ignoring safe image-based data URLs.

    Parameters
    ----------
    url_str : str
        The string to examine for dangerous URL schemes.

    Returns
    -------
    bool
        True if a dangerous scheme is detected, False otherwise.
    """
    if not isinstance(url_str, str):
        # Non‑string input cannot contain a scheme.
        return False

    # Patterns for dangerous schemes.  The pattern matches the start of a
    # URL, optionally preceded by whitespace and followed by a colon.
    # It is case‑insensitive to catch variants such as "JavaScript:".
    dangerous_pattern = re.compile(r'^\s*(javascript|vbscript)\s*:', re.IGNORECASE)

    # Search the entire string for a dangerous scheme.
    return bool(dangerous_pattern.search(url_str))