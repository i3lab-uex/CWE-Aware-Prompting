import re

def detect_js_scheme(url_string: str) -> bool:
    """
    Detects potentially dangerous URL schemes such as javascript or vbscript in a given string,
    while ignoring safe image data URLs.

    Args:
        url_string (str): The string to examine for possible dangerous URL schemes.

    Returns:
        bool: True if a dangerous scheme is detected, False otherwise.
    """
    # Trim leading/trailing whitespace
    url_string = url_string.strip()

    # Regex to capture the scheme before the first colon.
    # We use a non‑capturing group for the safe data:image scheme
    # and capture any other scheme.
    #
    #   - (?i)      : case‑insensitive matching
    #   - ^\s*      : start of string, optional whitespace
    #   - (?P<scheme>[a-z][a-z0-9+.-]*) : capture scheme (letters, digits, + . -)
    #   - \s*:\s*   : colon surrounded by optional whitespace
    pattern = re.compile(r'^\s*(?P<scheme>[a-z][a-z0-9+.-]*)\s*:', re.I)

    match = pattern.match(url_string)
    if not match:
        return False

    scheme = match.group('scheme').lower()

    # Exclude safe image data URLs (data:image/...)
    if scheme == 'data':
        # Verify that the media type is an image
        # e.g., data:image/png;base64,...
        if re.match(r'^data\s*:\s*image\/', url_string, re.I):
            return False
        # If data: but not image/*, treat as potentially dangerous
        return True

    # Dangerous schemes list
    dangerous_schemes = {'javascript', 'vbscript', 'data'}  # data is handled above
    return scheme in dangerous_schemes