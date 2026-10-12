import re

def detect_js_scheme(url_string: str) -> bool:
    """
    Detect whether a given string contains a potentially dangerous URL scheme
    (e.g., javascript:, vbscript:) while ignoring safe image data URLs.

    Parameters:
        url_string (str): The string to examine for dangerous URL schemes.

    Returns:
        bool: True if a potentially harmful scheme is found, False otherwise.
    """
    if not isinstance(url_string, str):
        # Non-string input cannot contain a URL scheme; treat as safe.
        return False

    stripped = url_string.lstrip().lower()

    # 1. Detect explicit javascript or vbscript schemes.
    if re.match(r'^(javascript|vbscript)\b', stripped):
        return True

    # 2. Handle data URLs.
    if stripped.startswith('data:'):
        # Extract the MIME type part (between 'data:' and the first ';' or ',').
        match = re.match(r'^data\s*:\s*([^;,]+)', stripped)
        if match:
            mime_type = match.group(1).strip()
            # If the MIME type starts with 'image/', treat as safe.
            if mime_type.startswith('image/'):
                return False
        # Any other data: URL (e.g., text/html, application/javascript) is dangerous.
        return True

    # 3. No dangerous scheme found.
    return False