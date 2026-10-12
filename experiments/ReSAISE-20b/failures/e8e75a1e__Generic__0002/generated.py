import re

def detect_malicious_url_scheme(url_string: str) -> bool:
    """
    Detect whether a URL string contains a potentially malicious scheme
    (e.g., javascript:, vbscript:) while ignoring valid image data URLs.

    Parameters:
        url_string (str): The URL string to inspect.

    Returns:
        bool: True if a dangerous scheme is detected, False otherwise.
    """
    if not isinstance(url_string, str):
        # Non-string input cannot contain a malicious scheme
        return False

    # Normalize leading whitespace and extract the first token up to ':'
    match = re.match(r'^\s*([a-zA-Z]+)\s*:?', url_string)
    if not match:
        return False

    scheme = match.group(1).lower()

    # Dangerous schemes
    dangerous_schemes = {"javascript", "vbscript"}

    if scheme in dangerous_schemes:
        return True

    # Handle data URLs
    if scheme == "data":
        # Extract the MIME type part (everything before first ';' or end)
        data_payload = url_string[len("data:") :]
        mime_part = data_payload.split(';', 1)[0].strip()
        # If MIME type starts with 'image/', it's a valid image data URL
        if mime_part.lower().startswith("image/"):
            return False
        # Otherwise treat as potentially dangerous
        return True

    return False