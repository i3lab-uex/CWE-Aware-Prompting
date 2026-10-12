import re

def verify_javascript_protocol(url_input: str) -> bool:
    """
    Detect potentially dangerous URL schemes in a string, excluding valid image data URLs.

    Parameters
    ----------
    url_input : str
        The string to examine for possible dangerous URL schemes.

    Returns
    -------
    bool
        True if the string starts with a harmful scheme (javascript:, vbscript:,
        or data: not referring to an image). False otherwise.
    """
    if not isinstance(url_input, str):
        return False

    # Strip leading whitespace for robust matching
    stripped = url_input.lstrip()

    # Check for javascript: or vbscript:
    if re.match(r'^(?:javascript|vbscript)\b', stripped, flags=re.IGNORECASE):
        return True

    # Check for data: URLs
    if re.match(r'^data\b', stripped, flags=re.IGNORECASE):
        # Accept only data:image/... URLs
        if re.match(r'^data\s*:\s*image\b', stripped, flags=re.IGNORECASE):
            return False
        return True

    return False