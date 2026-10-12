import re

def detect_malicious_url_scheme(url_string: str) -> bool:
    """
    Detects whether a given string contains potentially malicious URL schemes
    such as javascript:, vbscript: or other dangerous protocols, while ignoring
    valid image data URLs (e.g., data:image/png;base64,...).

    Parameters:
        url_string (str): The string to inspect.

    Returns:
        bool: True if a malicious scheme is found, False otherwise.
    """
    # Normalize the string for case‑insensitive matching
    lower = url_string.lower()

    # Exclude data URLs that are explicitly image types
    if re.search(r'^data:image\/[a-z0-9+\-.]+;base64,', lower):
        return False

    # List of dangerous schemes to detect
    dangerous_schemes = [
        r'javascript:',
        r'vbscript:',
        r'mshtml:',
        r'file:',
        r'exe:',
        r'dll:',
        r'ms-office:',
    ]

    # Build a regex pattern that matches any of the schemes at the start
    pattern = r'^\s*(' + '|'.join(dangerous_schemes) + r')'
    if re.search(pattern, lower):
        return True

    # Additional check for URLs that contain a scheme followed by colon
    # but not part of an allowed data URL.
    if re.search(r'^\s*([a-z][a-z0-9+\-.]*):', lower):
        scheme = re.match(r'^\s*([a-z][a-z0-9+\-.]*):', lower).group(1)
        if scheme in ('javascript', 'vbscript', 'mshtml', 'file',
                      'exe', 'dll', 'msoffice'):
            return True

    return False