import re

def verify_javascript_protocol(url_input: str) -> bool:
    """
    Detects potentially dangerous URL schemes (e.g., javascript:, vbscript:)
    while allowing safe image data URLs such as data:image/*.

    Parameters
    ----------
    url_input : str
        The string to examine for possible dangerous URL schemes.

    Returns
    -------
    bool
        True if a potentially harmful scheme is detected (excluding valid image data URLs),
        False otherwise.
    """
    if not isinstance(url_input, str):
        return False

    # Strip leading whitespace and capture the scheme part before ':'.
    match = re.match(r'^\s*([a-zA-Z][\w+\-.]*):', url_input)
    if not match:
        return False

    scheme = match.group(1).lower()

    # List of schemes considered dangerous.
    dangerous_schemes = {"javascript", "vbscript"}

    if scheme in dangerous_schemes:
        return True

    # Special handling for data URLs: only block if not an image.
    if scheme == "data":
        # Normalize the rest of the URL to check for 'image/' after data:
        # e.g., data:image/png;base64,...
        rest = url_input[match.end():].lstrip()
        if re.match(r'^image/', rest, flags=re.IGNORECASE):
            return False
        # Any other data: URL is considered dangerous.
        return True

    return False