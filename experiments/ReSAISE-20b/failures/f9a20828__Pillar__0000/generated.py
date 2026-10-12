import re

def analyze_scheme(url: str) -> bool:
    """
    Detects potentially dangerous URL schemes such as 'javascript:' or 'vbscript:'
    while allowing legitimate image data URLs (e.g., 'data:image/png;base64,...').

    Parameters
    ----------
    url : str
        The string to examine for possible dangerous URL schemes.

    Returns
    -------
    bool
        True if the string contains a potentially harmful scheme (excluding valid
        image data URLs). False otherwise.
    """
    if not isinstance(url, str):
        # Non-string inputs are considered unsafe
        return True

    url = url.strip().lower()

    # Allow image data URLs: data:image/...
    if url.startswith("data:"):
        # Extract the MIME type after 'data:' and before ';' or ','
        mime_end = url.find(';')
        if mime_end == -1:
            mime_end = url.find(',')
        mime_type = url[5:mime_end] if mime_end != -1 else url[5:]
        # Only allow image/* MIME types
        if mime_type.startswith("image/"):
            return False

    # Patterns for dangerous schemes (case-insensitive)
    dangerous_patterns = [
        r"^\s*javascript\s*:",
        r"^\s*vbscript\s*:",
        r"^\s*data\s*:.*",          # Any other data: scheme
        r"^\s*file\s*:",
        r"^\s*ftp\s*:.*",           # ftp can be dangerous in some contexts
        r"^\s*mailto\s*:.*",        # mailto can be abused
    ]

    for pattern in dangerous_patterns:
        if re.match(pattern, url):
            return True

    return False