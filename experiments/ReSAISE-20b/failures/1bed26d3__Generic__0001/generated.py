import re

def check_javascript_scheme(url_str: str) -> bool:
    """
    Detect if a string contains a potentially dangerous URL scheme
    (e.g., javascript:, vbscript:) while ignoring safe image data URLs.

    Parameters:
        url_str (str): The string to examine.

    Returns:
        bool: True if a dangerous scheme is detected, False otherwise.
    """
    if not isinstance(url_str, str):
        raise TypeError("url_str must be a string")

    # Remove leading/trailing whitespace
    trimmed = url_str.strip()

    # Capture the scheme at the beginning of the string.
    match = re.match(r'(?i)^\s*([a-z][a-z0-9+\-.]*):', trimmed)
    if not match:
        return False

    scheme = match.group(1).lower()

    # Schemes that are considered dangerous.
    dangerous_schemes = {"javascript", "vbscript", "data"}

    if scheme not in dangerous_schemes:
        return False

    # Special handling for data URLs: allow image/* types.
    if scheme == "data":
        # A safe image data URL starts with `data:image/`
        return not re.match(r'(?i)^data:image\/', trimmed)

    # For javascript and vbscript schemes, flag as dangerous.
    return True